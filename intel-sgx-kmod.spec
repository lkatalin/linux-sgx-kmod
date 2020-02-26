%if 0%{?fedora}
%global buildforkernels kmod
%global debug_package %{nil}
%endif

#test
Name:           intel-sgx-kmod
Summary:        Kernel module (kmod) for Intel SGX Out of Tree Driver
Version:        0.0.20200226
Release:        1%{?dist}
License:        Apache-2.0

Source0:        https://github.com/intel/linux-sgx-driver/archive/sgx_driver_2.6.tar.gz

BuildRequires:  kmodtool
%{!?kernels:BuildRequires: gcc, elfutils-libelf-devel, buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
This package contains the kmod module for the Intel SGX Out of Tree Driver.


%prep
%{?kmodtool_check}

# kmodtool output:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -c -T -a 0 -p 1

for kernel_version  in %{?kernel_versions} ; do
  cp -a intel-sgx-kmod-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*}/src modules
done


%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 -t %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/ $(find _kmod_build_${kernel_version%%___*}/ -name '*.ko')
 chmod u+x %{buildroot}%{_prefix}/lib/modules/*/extra/*/*
done
%{?kmod_install}


%changelog
* Wed Feb 26 2020 Lily Sturmann <lsturman@redhat.com> - 0.0.20200226-1
- Initial package
