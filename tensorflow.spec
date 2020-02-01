# TODO:
# - mkl_dnn only on %{x8664}
# - use system libs
# - fix install and packaging
#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Open source library for numerical computation using data flow graphs
Summary(pl.UTF-8):	Mająca otwarte źródła biblioteka do obliczeń numerycznych przy użyciu grafów przepływu danych
Name:		tensorflow
Version:	2.0.0
Release:	1
License:	Apache v2.0
Group:		Libraries
#Source0Download: https://github.com/tensorflow/tensorflow/releases
Source0:	https://github.com/tensorflow/tensorflow/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	86319b28bc9d0dc07685e09fcc79172e
Patch0:		%{name}-bazel.patch
URL:		https://tensorflow.org/
BuildRequires:	bazel
BuildRequires:	python3-devel >= 1:3.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TensorFlow is an open source software library for numerical
computation using data flow graphs. The graph nodes represent
mathematical operations, while the graph edges represent the
multidimensional data arrays (tensors) that flow between them. This
flexible architecture enables you to deploy computation to one or more
CPUs or GPUs in a desktop, server, or mobile device without rewriting
code. TensorFlow also includes TensorBoard data visualization toolkit:
<https://github.com/tensorflow/tensorboard>.

%description -l pl.UTF-8
TensorFlow to mająca otwarte źródła biblioteka do obliczeń
numerycznych przy użyciu grafów przepływu danych. Węzeł grafu
reprezentuje działania matematyczne, a krawędzie grafu reprezentują
wielowymiarowe tablice danych (tensory) przepływające między nimi. Ta
elastyczna architektura pozwala uruchamiać obliczenia na jednym lub
większej liczbie CPU lub GPU komputera osobistego, serwera lub
urządzenia przenośnego bez przepisywania kodu. TensorFlow zawiera
także narzędzia do wizualizacji danych TensorBoard:
<https://github.com/tensorflow/tensorboard>.

%package devel
Summary:	Header files for TensorFlow library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki TensorFlow
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for TensorFlow library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki TensorFlow.

%package static
Summary:	Static TensorFlow library
Summary(pl.UTF-8):	Statyczna biblioteka TensorFlow
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static TensorFlow library.

%description static -l pl.UTF-8
Statyczna biblioteka TensorFlow.

%prep
%setup -q
%patch0 -p1

%build
# choose one:
# - OpenCL SYCL: TF_NEED_OPENCL_SYCL=1 TF_NEED_COMPUTECPP=1?
# - ROCm: TF_NEED_ROCM=1
# - CUDA: TF_NEED_CUDA=1 TF_NEED_TENSORRT=1?
# MPI: TF_NEED+MPI=1
CC_OPT_FLAGS="%{rpmcflags}" \
HOST_C_COMPILER="%{__cc}" \
HOST_CXX_COMPILER="%{__cxx}" \
PYTHON_BIN_PATH="%{__python3}" \
PYTHON_LIB_PATH="%{py3_sitedir}" \
TF_DOWNLOAD_CLANG=0 \
TF_ENABLE_XLA=1 \
TF_NEED_CUDA=0 \
TF_NEED_MPI=0 \
TF_NEED_OPENCL_SYCL=0 \
TF_NEED_ROCM=0 \
TF_SET_ANDROID_WORKSPACE=0 \
%{__python3} configure.py

bazel build //tensorflow \
%ifnarch %{x8664}
	--config=mkl=false
%endif

%install
rm -rf $RPM_BUILD_ROOT

# FIXME: not make
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ACKNOWLEDGMENTS ADOPTERS.md AUTHORS ISSUES.md ISSUE_TEMPLATE.md README.md RELEASE.md SECURITY.md
%attr(755,root,root) %{_libdir}/libtensorflow.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtensorflow.so.N

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtensorflow.so
%{_includedir}/tensorflow

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtensorflow.a
%endif
