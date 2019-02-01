Tortuga 7.0 Installation and Administration Guide
=================================================

Univa Corporation \<support\@univa.com\>

January 2019 -- Version 1.4

About This Guide
----------------

This guide contains information for IT staff and end-users who will be
installing, configuring, and managing Tortuga 7.0. Information about
specific software kits is provided in the associated kit guides.

For detailed information on any Tortuga command, consult the standard
manual pages using `man <command>`. Manual pages are automatically
installed as part of the Tortuga software installation.

For those eager to get started, consult the "Quickstart" section for a
quick run-through a sample installation.

© 2008-2018 Univa Corporation. All rights reserved. This manual or parts
thereof may not be reproduced in any form or media without the express
written consent of Univa Corporation.

### Trademarks

All trademarks mentioned within this document are the property of their
respective owners.

Tortuga Quickstart
------------------

### Manual quickstart installation

#### Overview

This section describes a sample installation on Tortuga in three
different scenarios- on-premise, hybrid (on-premise + cloud-based using
Amazon EC2), and cloud-based using Amazon EC2.

**Note:** if installing on other cloud providers, such as [Google
Compute
Engine](https://cloud.google.com/compute "Google Compute Engine") or
[Microsoft Azure](https://azure.microsoft.com "Microsoft Azure"), the
basic installation procedure outlined below can be followed,
substituting the documented EC2-specific configuration for the
appropriate cloud provider resource adapter.

It is *strongly recommended* to read this manual prior to performing the
steps in this section.

Commands listed in this "Quickstart" section are intended to be run as
the `root` user on the Tortuga installer node.

### Prerequisites

#### General

-   CPU/RAM requirements

    The Tortuga installer requires a minimum of 8GB RAM and a modern
    64-bit CPU. A single-core is sufficient. Additional RAM and/or cores
    will offer increased Tortuga throughput and performance.

    For Amazon EC2-based installation, the instance type `m4.large` (or
    equivalent) is the suggested minimum.

-   Disk space requirements

    Not including the OS installation media (required only for
    on-premise compute node provisioning), Tortuga requires \<300MB of
    disk space.

    For installations supporting on-premise compute node provisioning
    *and* locally hosted OS installation media, the disk requirements
    increase to \<8GB.

-   Supported operating system

    Red Hat Enterprise Linux (RHEL) or CentOS 6.x or 7.x.

    RHEL/CentOS 7.x is *recommended*

    Tortuga installation has been validated tested on "official" RHEL
    and CentOS AMIs on Amazon EC2.

    If hosting the Tortuga installer on Amazon Web Services (AWS), refer
    to Tortuga AWS Identity & Access Management (IAM) role policy
    requirements.

-   Disable SELinux

    At the present time, Tortuga requires SELinux to be in *permissive*
    mode or disabled completely.

-   Synchronize system clock

    Tortuga depends on an accurate system clock during installation when
    SSL/TLS certificates for Puppet, HTTPs, etc. are created. Failure to
    sync the system clock may result in unexpected behaviour.

    ``` {.shell}
    yum -y install ntpdate
    ```

    Sync using a well-known time server. For example:

    ``` {.shell}
    ntpdate 0.centos.pool.ntp.org
    ```

-   (recommended) Refresh YUM package cache

    It is recommended to run `yum makecache fast` prior to installing
    Tortuga to ensure YUM package repositories are validated.

#### Installation specific requirements

-   On-premise installation

    -   Dedicated server or virtual machine for Tortuga installer node

        -   1 (or more) servers or virtual machines for Tortuga compute
            node(s)

        -   Compute nodes *must* be connected to Tortuga installer node
            through a *private* network

-   Hybrid (on-premise + cloud) installation

    -   (*optional*) VPN connection from on-premise to Amazon EC2

        Although not strictly necessary, it is recommended to have an
        externally managed, persistent VPN connection between on-premise
        network and Amazon.

        **Note:** Tortuga does not automatically set up or configure a
        VPN.

-   Amazon EC2-based installation

    -   Amazon EC2 authorization and credentials

        Amazon EC2 credentials are required when configuring the AWS
        resource adapter. These are used to allow Tortuga to manage AWS
        resources.

        The credentials used to configure the AWS resource adapter must
        be authorized to create/delete AWS resources (minimally Amazon
        EC2 and Amazon VPC).

        -   (*optional*) Amazon Virtual Private Cloud (VPC)

            Using an Amazon VPC allows the Tortuga installation to use
            an isolated section of the AWS cloud. Advanced features,
            such as the use of externally managed DNS server, require
            the use of an Amazon VPC.

        -   (*optional*) Enable 'optional' repository on RHEL

            When installing on Red Hat Enterprise Linux 6 or 7 (RHEL),
            it is necessary to enable the 'optional' repository to
            satisfy package dependencies.

            -   RHEL 6

                ``` {.shell}
                yum-config-manager --enable rhui-REGION-rhel-server-releases-optional
                ```

            -   RHEL 7

                ``` {.shell}
                yum-config-manager --enable rhui-REGION-rhel-server-optional
                ```

            -   RHEL 7 on AWS

                ``` {.shell}
                yum-config-manager --enable rhui-REGION-rhel-server-rhscl
                ```

### Quickstart Installation

1.  Extract Tortuga distribution tarball

    Copy Tortuga distribution to dedicated Tortuga server/instance and
    extract the Tortuga distribution tarball into the current directory:

    ``` {.shell}
    tar jxf tortuga*tar.bz2
    ```

    It may be necessary to install `bzip2` to extract the tarball:

    ``` {.shell}
    yum -y install bzip2
    ```

2.  Install Tortuga

    **Note:** if attempting to install Tortuga on a server where Tortuga
    (any version) has been previously installed, please refer to
    [Appendix C: Uninstalling Tortuga](#appendix-c-uninstalling-tortuga)
    before proceeding! It is *strongly recommended* to install Tortuga
    on a fresh installation of RHEL/CentOS.

    The base installation of Tortuga is performed in two steps. The
    first step performed by the `install-tortuga.sh` script creates the
    installation directory (`/opt/tortuga`; the installation directory
    currently cannot be changed. This will be addressed in a future
    Tortuga release)

    ``` {.shell}
    cd tortuga* && ./install-tortuga.sh
    ```

    The second step of Tortuga installation is the set up and
    configuration. This includes initializing the database, installation
    of default kit(s), initializing Puppet, etc.

    Assuming `install-tortuga.sh` ran without error, next run
    `tortuga-setup.sh` as follow:

    ``` {.shell}
    /opt/tortuga/bin/tortuga-setup --defaults
    ```

    **Note:** If the default network port settings used by Tortuga
    conflict with other service(s) in your installation environment, run
    `tortuga-setup` without the `--defaults` option and answer the
    prompts.

    **Hint:** if the installation fails for any reason, it can be
    restarted by specifying the `--force` option as follows:

    ``` {.shell}
    /opt/tortuga/bin/tortuga-setup <options> --force
    ```

    This will cause the installer to skip all checks and (hopefully)
    proceed without error. Typically the main reason why the setup might
    fail is due to network connectivity problems attempting to connect
    to the required YUM package repositories.

    At this point, the Tortuga installation is complete and ready to be
    configured.

    Before proceeding, apply environment changes as a result of the
    Tortuga installation:

    ``` {.shell}
    exec -l $SHELL
    ```

    This command will add all Tortuga CLIs and `puppet`, et al., to the
    system PATH as a result of files being added to `/etc/profile.d`.

3.  (*optional*) Enable local DNS server

    *On-premise/hybrid/custom cloud-based installations only*

    DNS services are provided on Tortuga using the
    [Dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html "Dnsmasq")
    DNS server.

    Enable the built-in Dnsmasq DNS server to resolve host names of
    Tortuga managed compute nodes.

    ``` {.shell}
    enable-component -p --no-sync dns
    /opt/puppetlabs/bin/puppet agent --verbose --onetime --no-daemonize
    ```

    While not required, it is also possible to enable local DNS name
    resolution to provide support for custom DNS domain names when
    Tortuga is hosted on EC2.

4.  (*optional*) Enable DHCP/TFTP server for PXE booting compute nodes

    *Required only for provisioning on-premise compute nodes*

    DHCP/TFTP is required to PXE boot on-premise compute nodes to use
    the Anaconda/Kickstart node provisioning mechanism.

    ``` {.shell}
    enable-component --no-sync -p dhcpd
    /opt/puppetlabs/bin/puppet agent --verbose --onetime --no-daemonize
    ```

5.  (*optional*) Add provisioning network interface

    *For installations with Tortuga-managed on-premises nodes only!*

    If enabling support for provisioning on-premises compute nodes, it
    is also necessary to add a provisioning network interface. Compute
    nodes will be provisioned using this interface to isolate traffic
    from the 'public' LAN.

    The argument to the `--nic` option is the network interface
    connected to the provsioning network. The provisioning network must
    be configured prior to adding nodes.

    ``` {.shell}
    add-nic --nic=eth1
    ```

    Use the `update-network` command to change provisioning network
    related settings.

6.  (*optional*) Install operating system media

    *Required only for provisioning on-premise compute nodes*

    Tortuga requires access to operating system media to install
    on-premise compute nodes.

    For example, to install CentOS mirror URL:

    ``` {.shell}
    install-os-kit --mirror --media http://<url to CentOS mirror>
    /opt/puppetlabs/bin/puppet agent --verbose --onetime --no-daemonize
    ```

    This will instruct Tortuga to proxy HTTP access to the provided
    CentOS mirror from Tortuga-managed compute nodes on the provisioning
    network without the need to enable NAT or have the provisioning
    network routed to the Internet.

    It is often desirable to create a local CentOS repository mirror for
    bandwidth and performance issues.

7.  Create software profile for compute nodes

    This software profile will be used to represent compute nodes in the
    Tortuga/Grid Engine cluster. The software profile name can be
    arbitrary.

    For on-premise compute nodes:

    ``` {.shell}
    create-software-profile --name execd
    ```

    For cloud-based compute nodes:

    ``` {.shell}
    create-software-profile --name execd --no-os-media-required
    ```

    The option `--no-os-media-required` allows creation of a software
    profile without an association to (local) installation media. Since
    cloud-based instances already have an operating system installed, it
    is not necessary to define the installation media.

    **Note**: Software profiles are created with a default max nodes
    setting of 25. To change or remove this limit:

    ``` {.shell}
    update-software-profile --name execd --max-nodes XX
    ```

    Where `XX` is the maximum number of nodes you want to allow. To
    remove the limit altogether, use `none`. See the section on software
    profiles below for more information.

8.  Create hardware profile for compute nodes

    This hardware profile will used to represent compute nodes in the
    Tortuga/Grid Engine cluster. The hardware profile name is arbitrary.

    For on-premise nodes and cloud-based nodes in a hybrid installation:

    ``` {.shell}
    create-hardware-profile --name execd --defaults
    ```

    The `--defaults` option instructs Tortuga to use the provisioning
    network when adding nodes to this hardware profile.

    For cloud-based installations:

    ``` {.shell}
    create-hardware-profile --name execd
    ```

9.  Map software and hardware profiles

    Profiles must be mapped in order for Tortuga to identify a valid
    compute node provisioning configuration.

    ``` {.shell}
    set-profile-mapping --software-profile execd --hardware-profile execd
    ```

10. (*optional*) Configure Anaconda/Kickstart file template

    *On-premise compute nodes only*

    Prior to adding compute nodes, it is recommended to configure the
    root password in the Kickstart file template
    (`$TORTUGA_ROOT/config/kickstart.tmpl`).

    The root password setting is found under `rootpw` in the Anaconda
    Kickstart template file.

    Kickstart Syntax Reference can be found in the Red Hat Enterprise
    Linux Installation Guide. Several configuration options can be set
    in the Kickstart file template which will affect all Tortuga
    provisioned physical/virtual compute nodes.

11. (*optional*) Install AWS resource adapter

    *Hybrid and EC2-based installations only*

    If using an alternate cloud provider, substitute the appropriate
    resource adapter kit here, along with resource adapter
    configuration.

    Installing the AWS resource adapter allows provisioning of compute
    nodes on Amazon EC2.

    ``` {.shell}
    install-kit --i-accept-the-eula kit-awsadapter-*.tar.bz2
    enable-component -p --no-sync awsadapter-7.0.3-0 management-7.0.3
    ```

    1.  Configure AWS resource adapter

        The `adapter-mgmt` command is used to manage resource adapter
        configuration profiles for all Tortuga supported resource
        adapters. In this example, we are configuring the `AWS` resource
        adapter:

        ``` {.shell}
        adapter-mgmt create --resource-adapter AWS \
            --profile default \
            --setting region=<AWS region name> \
            --setting awsAccessKey=<AWS access key> \
            --setting awsSecretKey=<AWS secret key> \
            --setting keypair=<AWS keypair name> \
            --setting ami=<ami-XXXXXXXX> \
            --setting instancetype=<AWS instance type> \
            --setting user_data_script_template=<bootstrap script template> \
            --setting securitygroup=<AWS security group>
        ```

        When using IAM (AWS-specific), the settings `awsAccessKey` and
        `awsSecretKey` can be omitted as the credentials to manage
        instances will be automatically provided through the current IAM
        profile.

        If using Amazon VPC, the `subnet_id` in the desired VPC must be
        specified:

        ``` {.shell}
        adapter-mgmt create --resource-adapter AWS \
            --profile default \
            <settings from above..>
            --setting subnet_id=<subnet-XXXXXXXX>
        ```

        The AWS region setting (`region`) defaults to `us-east-1` if not
        provided.

        The list of available regions can be obtained from
        <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html>
        or from the AWS CLI using `aws ec2 describe-regions`.

        **Note:** settings for `ami` and `securitygroup`, and
        `subnet_id` (if applicable) are dependent on the `region`
        setting. Ensure the specified `ami` and `subnet_id` are in the
        specified region.

        If the Tortuga installer is hosted on EC2, the specified
        security group must allow unrestricted access to all instances
        within the same security group (ie. installer and compute
        instances. Alternatively, specific ports may be opened as
        documented in [Firewall Configuration](#firewall-configuration)
        below.

        Use one of the following values for `user_data_script_template`:

        -   `bootstrap.tmpl` for RHEL/CentOS 6 & 7 instances
        -   `bootstrap.python3.tmpl` for Fedora 23/24/25
        -   `bootstrap.amazonlinux.tmpl` for recent Amazon Linux
            versions
        -   `bootstrap.debian.tmpl` for recent Debian/Ubuntu versions
        -   `bootstrap.suse.tmpl` for SUSE Linux/openSUSE versions

        `adapter-mgmt update` can be used to manage resource adapter
        configuration profile settings. Erroneous/invalid settings can
        be removed by using
        `adapter-mgmt update PROFILENAME --delete NAME`, where `NAME` is
        the setting name.

    2.  Create hardware profile to represent EC2 nodes

        For EC2-based Tortuga installer:

        ``` {.shell}
        create-hardware-profile --name execd-aws
        ```

        or for hybrid installation:

        ``` {.shell}
        create-hardware-profile --name execd-aws --defaults
        ```

        The `--defaults` argument requires the provisioning network
        being set up in an earlier steps.

        Configure newly created hardware profile for use with Amazon
        EC2:

        ``` {.shell}
        update-hardware-profile --name execd-aws \
            --resource-adapter AWS --location remote
        ```

        When running with an EC2-based Tortuga installer, it is *also*
        necessary to set the hardware profile name format so
        EC2-assigned host names are used:

        ``` {.shell}
        update-hardware-profile --name execd-aws --name-format "*"
        ```

    3.  Map hardware and software profiles

        Because the software profile "execd" was previously created and
        can be shared between local nodes/virtual machines and EC2-based
        instances, it is not necessary to create another software
        profile.

        Map EC2 hardware profile to existing "execd" software profile:

        ``` {.shell}
        set-profile-mapping --software-profile execd \
            --hardware-profile execd-aws
        ```

12. Install Univa Grid Engine

    Now that the Tortuga base installation is complete, it is necessary
    to install Univa Grid Engine.

    In this example, the Grid Engine `qmaster` will be run on the
    Tortuga installer node.

    1.  Install UGE kit

        ``` {.shell}
        install-kit kit-uge*.tar.bz2
        ```

    2.  Create default Grid Engine cluster

        The command `uge-cluster` is used to configure UGE clusters
        under Tortuga. In this example, the UGE cell/cluster is named
        "default".

        ``` {.shell}
        uge-cluster create default
        uge-cluster update default \
            --add-qmaster-swprofile Installer
        uge-cluster update default \
            --var sge_cell_netpath="%(qmaster)s:%(sge_root)s/%(cell_name)s"
        uge-cluster update default --var manage_nfs=false
        ```

    3.  Enable Grid Engine `qmaster` component on Tortuga installer.

        ``` {.shell}
        enable-component -p --no-sync qmaster
        /opt/puppetlabs/bin/puppet agent --onetime --verbose --no-daemonize
        ```

    4.  Validate installation of `qmaster`

        It is recommended to validate the installation of the `qmaster`.

        Check the version of UGE kit that was installed, either by
        looking for the version in the kit's file name or by running

        ``` {.shell}
        ls -ld /opt/uge-*
        ```

        For example, if the installed version is `8.6.4`, source the
        environment by running:

        ``` {.shell}
        . /opt/uge-8.6.4/default/common/settings.sh
        ```

        **Hint:** Use the UGE `qhost` command to display list of hosts
        known to the UGE cluster.

    5.  NFS export the default Grid Engine spool directory

        Install NFS support, if necessary:

        ``` {.shell}
        yum -y install nfs-utils
        ```

        Ensure NFS server service is running:

        RHEL/CentOS 6.x:

        ``` {.shell}
        service nfs restart
        ```

        or RHEL/CentOS 7.x:

        ``` {.shell}
        systemctl restart nfs
        ```

        Add the following entry to `/etc/exports`:

        ``` {.shell}
        /opt/uge-8.6.4 *(rw,async)
        ```

        Finally, export the filesystem:

        ``` {.shell}
        exportfs -a
        ```

    6.  Enable `execd` component on software profile(s)

        Enabling the `execd` component will make nodes in the "execd"
        software profile automatically part of the UGE cluster.

        ``` {.shell}
        enable-component --software-profile execd --no-sync execd
        ```

    7.  Update UGE cluster configuration

        ``` {.shell}
        uge-cluster update default --add-execd-swprofile execd
        ```

13. Adding compute nodes

    To add nodes to the on-premise Tortuga/UGE cluster or physical nodes
    in hybrid installation use the `add-nodes` command as follows:

    ``` {.shell}
    add-nodes --count 3 \
        --software-profile execd --hardware-profile execd
    ```

    Add nodes on EC2-based Tortuga installation:

    ``` {.shell}
    add-nodes --count 3 \
        --software-profile execd --hardware-profile execd-aws
    ```

    Check status of newly added node(s) using the `get-node-status`
    command.

    Once the node has reached **Installed** state, it is available to be
    used.

    Nodes will be created momentarily and automatically added to the UGE
    cluster. Use `qhost` to display UGE cluster host list. It can take a
    few minutes until load values show up for newly added nodes.

About Tortuga
-------------

In today's datacenter, it is no longer sufficient to simply install and
configure systems, then hand them over to users. Maintenance and
upgrades require frequent adjustments, hardware advances arrive faster
than ever, and IT staff are expected to provide users with the "latest
and greatest" technologies without interrupting their work.

In recent years, the adoption of *virtualization* and mainstream arrival
of *cloud computing* have improved datacenter efficiently exponentially.
Multiple users can now simultaneously access a system in a truly secure
manner. Previously unused capacity can be recaptured, and costs are
reduced as datacenter capacity can more closely align with actual need.

Virtualization allows a datacenter to evolve into a *private cloud*,
where users make requests for computing resources, the datacenter
fulfills those requests, and jobs get done without planning around
downtime and interruptions.

Companies with limited resources have access to options which limit the
need for maintaining physical datacenters. Various *public cloud*
services offer a virtually unlimited resource pool of on-demand
computing and storage resources, with pay-as-you-go and
subscription-based offerings.

The most flexible datacenter combines these options, providing a private
cloud and utilizing resources from public clouds for extra capacity
on-demand. This *hybrid cloud* approach offers a kind potential which is
only beginning to be realized.

Tortuga is a *cloud orchestration and management system* which
integrates with public and private clouds, automating the allocation of
resources and their software configurations. Unlike other solutions,
Tortuga offers a single, consistent interface regardless of the
underlying API or control panel.

Leveraging the power and flexibility of the open-source *Puppet*
configuration management tool, Tortuga brings the full power of Puppet
to handle complex software configuration management. Nodes can be
reconfigured on the fly or pre-configured before installation, all
on-demand.

Software "kits" add the ability for Tortuga to automate almost any kind
of decision based upon any criteria. Tortuga can reconfigure datacenters
automatically, making adjustments based on customized metrics, cost, or
performance. Tortuga can optimize resources as and when needed.

Tortuga also fulfills the promise of *hybrid clouds* by offering usable
*cloud bursting*. Unlike manual configurations where users must consider
where nodes are physically located and how to access them, Tortuga sets
up a secure VPN so users see everything as part of a single datacenter.
There is no need to know about different APIs or access mechanisms.

On top of what it can already do, Tortuga is also an extensible
platform. It supports new capabilities which are specific to an
organization's proprietary needs. Since Tortuga is written in
[Python](http://python.org) and uses
[Puppet](http://puppet.com "Puppet"), it is easy to create recipes and
scripts to handle unique datacenter requirements.

Here are just a few examples of what Tortuga can do. Note that some of
these examples require the installation of additional, optional software
kits from Univa:

-   Automatically install an operating system, then install and
    configure application software on a physical computer over the
    network (OS and application software stack provisioning).
-   Create and manage virtual machines on a local hypervisor in a
    datacenter.
-   Request and manage nodes hosted in a public cloud service such as
    [Amazon EC2](https://aws.amazon.com/ec2/ "Amazon EC2") or a local
    cloud, such as [OpenStack](http://openstack.org "OpenStack").
-   Integrate with application software and reconfigure systems based on
    cost, current use, or any kind of end-user customized metric.
-   Enable "cloud bursting" to get users' the critical resources needed
    to complete a time-sensitive project on-time and on-budget,
    especially when the time and cost associated with traditional
    methods of purchasing and installing new hardware are impractical.

Supporting the Datacenter Lifecycle
-----------------------------------

Tortuga assists in performing common tasks supporting the lifecycle of a
datacenter server.

Tortuga can *provision* physical hardware with an operating system and
software application stack.

Tortuga abstracts complex virtualization APIs to *manage virtual
machines* using a single, consistent interface.

Tortuga performs *reallocation* of "compute" nodes from one task to
another.

Tortuga obtains resources from clouds to *cloud burst*, virtually
integrating public and private clouds into a single, unified, secure
datacenter.

Understanding Tortuga Architecture
----------------------------------

Tortuga treats datacenters, virtual machines, and cloud computing
resources or *instances* as a *cluster*. Unlike the traditional use of
this term, however, Tortuga clusters can be subdivided to cater to
specific users, tasks, or functions.

Clusters in Tortuga are collections of *nodes*. A node is simply a
representation of a machine, be it a physical computer, a virtual
machine, or a cloud resource. Nodes can even be 'placeholders' used to
pre-approve the allocation of cloud resources without actually starting
them, avoiding usage charges.

Most nodes in Tortuga are called *compute nodes*, regardless of what
task they are performing. There is also a special node, called the
*installer node* (also sometimes referred to as the "primary
installer"), which is the node actually running the Tortuga software. It
is responsible for managing the cluster, the software applications
running on nodes, and can also provision nodes.

Nodes in Tortuga are managed through the definition of *hardware
profiles* and *software profiles*. These profiles tell Tortuga how nodes
should be configured (or even if they should be managed by Tortuga at
all), and are the building blocks used to manage a cluster.

Detailed Installation Guide
---------------------------

### Hardware and Software Requirements

The first step in installing Tortuga is to select a machine for use as
the *installer node*. This can be a physical machine or a virtual
machine and must already be running a supported operating system
(RHEL/CentOS 6.x or 7.x).

It is *strongly recommended* that Tortuga be installed on a dedicated
server. It may co-exist with an existing dedicated UGE qmaster host.

#### CPU

Tortuga supports any modern x86-architecture 64-bit CPU. Larger clusters
benefit from more powerful processors as more incoming requests can be
handled simultaneously.

#### Memory

Tortuga requires a minimum of 8 GB. Additional memory can improve system
throughput and handling of requests from nodes in the cluster, and
improves the efficiency of the installer.

### Operating Systems

Tortuga officially supports the following operating systems:

-   Red Hat Enterprise Linux x86-64 7.x and 6.x
-   CentOS x86-64 7.x and 6.x

### Network

Tortuga requires an IP-enabled network.

Any IP networking configuration supported by the host operating
system(s) is supported.

### Disk Space

Tortuga requires less than 200MB of disk space for the core software.
The actual disk space needed may be higher, if additional OS package
dependencies must also be installed.

If configured for physical or virtual node provisioning, Tortuga will
require additional disk space to store OS packages in a repository. This
will depend on both the number and size of the operating systems being
provisioned. For example, the two CentOS 6.x installation DVDs require
*approximately* 5GB of disk space.

This space requirement can be reduced by using symbolic links,
NFS-mounted directories, and networked HTTP proxy repositories. See the
documentation for configuring node provisioning for further details.

### Hypervisor/Cloud Support

Tortuga supports the following cloud and virtualization platforms:

-   [Amazon Elastic Compute Cloud
    (EC2)](https://aws.amazon.com/ec2/ "Amazon EC2")
-   [Google Compute
    Engine](https://cloud.google.com/compute "Google Compute Engine")
-   [Microsoft Azure](https://azure.microsoft.com "Microsoft Azure")
-   [OpenStack](http://openstack.org "OpenStack")
-   VMware vSphere® versions 5.x

Support for hypervisors/virtualization and public clouds is provided
through the installation of additional software feature "kits".

Resource adapter "kits" are not automatically installed as part of the
base Tortuga software and may be installed after the base installation.

Refer to the documentation for the kit for any additional requirements.

### Compute Node Requirements

Tortuga does not impose restrictions on the hardware or software
required for compute nodes. The operating system and application
software to be installed on nodes in the cluster (if any) determines
these requirements.

### Preparing For Installation

#### Configuring Network Access

The base Tortuga installation has minimal network topology requirements.
If Tortuga will be used to provision compute nodes, additional network
setup will be required after the core Tortuga software is installed and
configured.

Tortuga includes the ability to provision physical nodes in the base
installation. It supports flexible network configurations in this mode.
For example, it supports multi-homed systems providing Internet and
local network access on separate network cards. It also supports systems
using a single network card with multiple VLANs providing these
functions.

Regardless of network configuration, the installer must have a
fully-qualified domain name (FQDN) resolvable via DNS. This can be
verified by observing that the output of `hostname --fqdn` is a
full-qualified domain name in the format `hostname.domainname`.

Likewise, the command `hostname --domain` must return a valid DNS domain
name before proceeding with the installation.

If either of these commands do not return the correct values, some
common resolutions include:

1.  Adding an entry to `/etc/hosts` for the host name with the following
    format:

    ``` {.shell}
    a.b.c.d     hostname.domainname hostname
    ```

2.  Defining the installer's FQDN in `/etc/sysconfig/network` using the
    directive `HOSTNAME="..."`.

    Note: changing this setting requires a system reboot in order for
    the change to take effect.

3.  Configuring the DNS server specified in `/etc/resolv.conf` to
    resolve the installer's name as a fully-qualified DNS name.

4.  Configuring the public DHCP server (if one is used) to issue the
    proper FQDN to the system when it requests its IP address.

The Tortuga installation program requires Internet access to download
packages from Puppet Labs,
[EPEL](https://fedoraproject.org/wiki/EPEL "EPEL"), and packages in the
[Python Package Index (pypi)](https://pypi.python.org). Compute nodes do
not normally require access to the Internet, as they typically retrieve
packages from the installer.

Once Tortuga is configured and operational, the installer no longer
requires Internet access. Additional software kits may require Internet
access during their installation and configuration to resolve
dependencies, however.

#### Firewall Configuration

It is recommended that any system-level firewall be disabled on both the
Tortuga installer and compute nodes during the initial installation.
Once a baseline level of functionality has been established, it is
possible to re-enable the firewall.

To disable the firewall, run the following commands as `root` on
RHEL/CentOS 6.x:

``` {.shell}
/etc/init.d/iptables save
/etc/init.d/iptables stop
chkconfig iptables off
```

or on RHEL/CentOS 7.x:

``` {.shell}
systemctl stop firewalld
systemctl disable firewalld
```

The following ports *must* be open for ingress on the Tortuga installer
and egress on the Tortuga-managed compute nodes:

     Port  Protocol  Description
  ------- ---------- ----------------------------------------------------------------------------------------------------------------------------
       22    tcp     ssh
       53  udp/tcp   DNS
       67  udp/tcp   DHCP (only req'd for on-premises node provisioning)
       68  udp/tcp   DHCP (only req'd for on-premises node provisioning)
      111  udp/tcp   rpcbind (req'd for NFS)
     2049  udp/tcp   NFS
     6444    tcp     Grid Engine qmaster *default*
     6445    tcp     Grid Engine execd *default*
     8008    tcp     Tortuga "internal" web server
     8140    tcp     Puppet server
     8443    tcp     Tortuga web service
    61614    tcp     [ActiveMQ](http://activemq.apache.org/ "ActiveMQ") (req'd by [MCollective](https://puppet.com/mcollective/ "MCollective"))

**Note:** it may be necessary to open additional ports depending on
system configuration and/or applications in use.

**Warning:** An overly restrictive firewall can cause connectivity
issues in a cluster if not properly configured. As a first
troubleshooting step, if possible, temporarily disable the firewall if
network connectivity issues are suspected.

#### Puppet

A standalone [Puppet](http://puppet.com "Puppet") Server is
automatically installed during Tortuga installation.

Tortuga has been tested and validated against
[Puppet](http://puppet.com "Puppet") 4.9.0. Newer versions of Puppet 4.x
*should* generally work without problem, and will be tested for official
support as they are released.

If required, different versions of [Puppet](http://puppet.com "Puppet")
may be used on compute nodes. This may be useful for configurations
where Tortuga will not be provisioning the operating system for nodes,
or for imaged node provisioning. In this case, all compute nodes must
have a Puppet version equal to or greater than the version on the
installer node.

The default installation hosts a [Puppet](http://puppet.com "Puppet")
master (server), including
[ActiveMQ](http://activemq.apache.org/ "ActiveMQ"), and
[MCollective](https://puppet.com/mcollective/ "MCollective").

#### OS Package Repositories

Tortuga requires access to OS repositories to resolve software
dependencies. These repositories, including any for paid/registered OS
support, must be installed and configured *prior* to installation.

Access to [EPEL](https://fedoraproject.org/wiki/EPEL "EPEL") or
[Puppet](http://puppet.com "Puppet") repositories is handled internally
by the Tortuga installer and need not be pre-configured.

The command `yum search kernel` can verify access to OS package
repositories. If this command does not list a number of packages,
including `kernel.x86_64`, the OS package repositories are not
configured correctly and Tortuga installation will fail.

[Red Hat Enterprise Linux](#red-hat-enterprise-linux) (RHEL) users must
ensure the "optional" repository is enabled. Assuming the node has been
registered with Red Hat Network, this repository can be enabled using
`yum-config-manager` (from the `yum-utils` package):

RHEL 7 Server:

``` {.shell}
yum-config-manager --enable rhel-7-server-optional-rpms
```

RHEL 7 Server on AWS:

``` {.shell}
yum-config-manager --enable rhui-REGION-rhel-server-optional
```

RHEL 6 Server:

``` {.shell}
yum-config-manager --enable rhel-6-server-optional-rpms
```

RHEL 6 Server on AWS:

``` {.shell}
yum-config-manager --enable rhui-REGION-rhel-server-releases-optional
```

#### SELinux

Tortuga is **not** compatible with SELinux when in "Enforcing" mode.

Please ensure SELinux is in "Permissive" mode or disabled entirely.

The file `/etc/sysconfig/selinux` contains the configuration for
SELinux.

**Hint:** Use `setenforce Permissive` to disable SELinux until the next
reboot, but be sure to update `/etc/sysconfig/selinux` to have the
setting persist after reboot.

### Installing Tortuga

*NOTE: Tortuga **must** be installed as the `root` user.*

#### Unarchiving and Installing the Software

Tortuga is distributed as a `bzip2` compressed tar file. Install `bzip2`
as follows, if necessary:

``` {.shell}
yum install bzip2
```

Unpack the software and change to the directory containing the software
as follows:

``` {.shell}
tar xjf tortuga-*.tar.bz2
cd tortuga-*
```

Begin the installation process by running the installation script in
that directory:

``` {.shell}
./install-tortuga.sh
```

[SQLite](http://sqlite.org "SQLite") is used as the default backing
database.

The installer accepts a few options, which can be viewed by running
`./install-tortuga.sh --help`. The important options are:

-   `--verbose` or `-v` to enable more detailed output.
-   `--force` to force the installer to run even if the `$TORTUGA_ROOT`
    directory already exists; this should only be used if an error
    occurred and the installer now refuses to run.

Installing Tortuga takes several minutes. The actual time required
depends on the speed of the installer's Internet connection and what
dependencies must be installed.

**NOTE:** [EPEL](https://fedoraproject.org/wiki/EPEL "EPEL") and
[Puppet](http://puppet.com "Puppet") repositories will, on occasion,
fail to respond, causing transient errors and installation failure. If
this happens, verify the OS repositories (see above), then re-run the
installer. It can sometimes take several attempts before the external
repositories respond.

#### Running `tortuga-setup`

*NOTE: tortuga-setup **must** be run as the 'root' user*

`tortuga-setup` configures Tortuga to run on the installer. Setup times
are dependent upon system speed, and generally range from 5-15 minutes.

Before running setup, source the Tortuga environment. Setup will install
the environment in `/etc/profile.d` so it is automatically available to
new shells or terminals.

To run setup:

``` {.shell}
/opt/tortuga/bin/tortuga-setup
```

After accepting the software EULA (required to proceed), answer the
following questions:

1.  What location should be used as the depot directory? (default
    `/opt/tortuga/depot`)
2.  What administrative username and password should be used?

The 'depot directory' is used by Tortuga to store (mostly package) files
required by compute nodes provisioned by Tortuga. Multiple YUM
repositories will be created in this directory. The disk space required
depends on the number of operating systems installed for provisioning,
as well as what optional software kits are added.

The depot directory may be mounted from a remote server, provided it is
mounted automatically upon boot and allows full access to the root user.
This generally means you must disable root squash on an NFS-exported
volume, although it may be possible to map root to a user with full
access to the volume.

Tortuga maintains its own user namespace. These users can be designated
as administrators of specific hardware and software profiles. The
default Tortuga installation has a single administrator. Tortuga users
can be added, deleted, and passwords changed, after setup is complete.

Tortuga Fundamentals
--------------------

Command-line interface
----------------------

Tortuga offers a command-line interface usable for scripting, with all
commands contained in the directory `$TORTUGA_ROOT/bin`. The
installation program installs manual pages accessible via the standard
Linux `man <command>` syntax.

Useful options accepted by all Tortuga commands include:

-   `-h`, `-?`, or `--help` -- display a summary of options supported by
    the command
-   `-v` -- print the version of the Tortuga command and exit
-   `--username USERNAME` -- Specifies a Tortuga username
-   `--password PASSWORD` -- Specifies a Tortuga password

### Software and Hardware profiles

Software and hardware profiles are used to manage logical groupings of
similar nodes in Tortuga.

#### Hardware profiles

##### Hardware profiles overview

A *hardware profile* tells Tortuga about *what* and *where* a node is,
be it physical, virtual, or cloud-based. The hardware profile gives
Tortuga the information it must know to manage the node - for example,
what virtualization or cloud provider might be used.

Hardware profiles also specify the default operating system kernel.
Since public cloud providers frequently bundle hardware information with
a base software image, this allows Tortuga to properly manage them. For
example, Amazon EC2 specifies an 'AMI' which not only dictates things
like disk storage, but also a complete image of the root filesystem and
kernel.

The hardware profile of a node cannot be changed.

Tortuga creates a hardware profile called `Installer` automatically.
This profile is specifically reserved for use by the installer, and
should not be used for other nodes. It cannot be modified or deleted.

##### Creating Hardware Profiles

Hardware profiles are created using the `create-hardware-profile`
command.

For example, to create a hardware profile using the default hardware
profile template:

``` {.shell}
create-hardware-profile --name LocalIron
```

This command will create a hardware profile that represents physical
nodes.

The following arguments are optional:

-   `--name <NAME>` -- The name of the hardware profile. Best kept to a
    short descriptive name such as "LocalIron" or "Mfg\_model\_500".
-   `--description <DESCRIPTION>` -- A human-readable description of the
    intended use for the hardware profile. Stored, but not interpreted,
    by Tortuga. The description may contain spaces, if quoted.
-   `--os <name-version-arch>` -- If provisioning is enabled and
    multiple OS kits are installed, this selects the OS for the profile.
    If unspecified, the OS running on the installer node is used.
-   `--idleSoftwareProfile <PROFILENAME>` -- Used for physical nodes. If
    a node is idled using the `idle-node` command, it is forced into
    this software profile.

Idle profiles are useful when a software profile (see below) includes an
application with an "expensive" or limited license. When the node is
idled, the idle profile eliminates the application from the node,
freeing up the license. This is generally unnecessary for virtual
machine nodes, which are deleted entirely instead of idled.

The nodes using a given hardware profile do not actually need to have
*identical* hardware. They must, however, be interchangeable in terms of
how they can be managed (created, deleted, turned on or off, etc) at the
hardware level.

Virtual machines which will be created and managed outside of Tortuga
should be treated as physical machines. Tortuga does not 'detect' if a
node is physical or virtual.

##### Network Settings

Before a hardware profile can be used, it must have an associated
provisioning NIC and network. This identifies the network settings for
all nodes created in that hardware profile and defines the connectivity
between the Tortuga installer and compute nodes.

The network parameters are set using `update-hardware-profile` and the
options `--add-provisioning-nic` and `--add-network` to associate a
provisioning NIC and network, respectively.

For example, when provisioning VMware vSphere-based compute nodes, if
the provisioning NIC (that is, the NIC connected to the
provisioning/management network on the Tortuga installer) has an IP
address `10.0.0.1` and the provisioning/management network is
"10.0.0.0/255.255.255.0", the following command-line would be used:

``` {.shell}
update-hardware-profile --name PROFILE --add-provisioning-nic 10.0.0.1 \
    --add-network 10.0.0.0/255.255.255.0/eth0
```

Effectively, this command sets up the specified hardware profile to be
connected to the Tortuga installer via the network interface with the IP
address *10.0.0.1* on the network *10.0.0.0/255.255.255.0*.

Note: the device name `eth0` reflects the name of the NIC **on the
compute node**, not the device name of the provisioning NIC on the
installer.

Traditionally, the public network device name on the Tortuga installer
would be `eth0` and the provisioning/management network device name
would be `eth1`.

##### Updating hardware profile settings

The list of current hardware profiles is given by
`get-hardware-profile-list`. Detailed information is available using
`get-hardware-profile --name <HWPROFILENAME>`.

To modify a hardware profile, use `update-hardware-profile`. Most fields
can be updated, but things set during provisioning (such as the OS,
kernel, and name format) will only take effect for *future* nodes, not
*existing* nodes.

The following command changes the host name format of the hardware
profile `Rack2`:

``` {.shell}
update-hardware-profile --name Rack2 --name-format rack2-#NN
```

Nodes not provisioned and/or managed by Tortuga can be added by setting
the hardware profile location to be "remote", using the command
`update-hardware-profile --name <NAME> --location remote`. This is
useful in cases where Tortuga must be aware of, but not necessarily
manage, a node. For example, this allows the addition of externally
managed hypervisors and/or other infrastructure nodes to the cluster.

Hardware profiles used for virtual machines require a hypervisor
software profile. The relationship of (hardware profile) virtual
machine, hosted by a (software profile) hypervisor, running on a
(hardware profile) physical machine, is configured using:

``` {.shell}
update-hardware-profile --name <NAME> --hypervisor-profile PROFILE
```

Additionally, virtual machine hardware profiles require a *resource
adapter*, used to manage the hypervisor. This is done using the
`--resource-adapter <ADAPTER>` option and tells Tortuga what API will be
used for management. See the kit documentation supplying the resource
adapter for more details.

The command `get-resource-adapter-list` lists available resource
adapters.

#### Deleting hardware profiles

Hardware profiles can be deleted using the `delete-hardware-profile`
command. Hardware profiles cannot be deleted until associated nodes
nodes are first deleted.

``` {.shell}
delete-hardware-profile --name Rack2
```

#### Software profiles

##### Software Profiles Overview

A *software profile* describes the software "stack" or configuration
(applications + operating system), as well as the disk setup for a
managed node.

The software profile also indicates the components (defined within
software kits) that should be enabled and configured.

Nodes are added to software profiles when they are added to the cluster.
Unlike the associated hardware profile, the software profile associated
with a node can be changed at any time. When the software profile of a
node is changed, the entire node, including the operating system, is
reinstalled to ensure the software configuration is "clean".

The software profile `Installer` is automatically created when Tortuga
is first installed. This profile is specifically reserved for use by the
installer, and should *not* be used to provision additional nodes.
Components may be enabled and disabled on this profile to configure
features, but the profile cannot be deleted.

#### Display list existing software profiles

The list of current software profiles is given by
`get-software-profile-list`.

#### Display software profile detail

Use `get-software-profile --name <NAME>` to display information about
specified software profile.

The command `get-software-profile --name <NAME> --json` will output the
software profile in JSON format. This can be redirected to a file and
used as a software profile template as described below.

#### Creating a software profile

Create software profiles using the \`create-software-profile command.

The following arguments are optional:

-   `--template <PATH>` -- Full path to JSON software profile template
-   `--name <NAME>` -- The name of the software profile. Best kept to a
    short descriptive name such as "AppName" or "Engineering\_Dept".
-   `--description <DESCRIPTION>` -- A human-readable description of the
    intended use for the software profile. Stored, but not interpreted,
    by Tortuga. The description may contain spaces, if quoted.
-   `--os <name-version-arch>` -- If provisioning is enabled and
    multiple OS kits are installed, this selects the default OS for the
    profile. This option requires that the hardware profile used allows
    the software profile to override the OS spec.

If the JSON software profile template is not specified, a barebones
software profile is created. **Note:** the barebones software profile
may not contain sufficient parameters to provision some nodes (ie.
on-premise/physical).

##### Examples

The following command will create a software profile named `Compute`
provisioned with the same operating system as the Tortuga installer:

``` {.shell}
create-software-profile --name Compute
```

It is also possible to create software profiles for different operating
systems (assuming the OS kit has already been installed. See below for
more details). This command would set the operating system of nodes
created in the `Compute` software profile to RHEL 7.5 x86\_64:

``` {.shell}
create-software-profile --name Compute --os rhel-7.5-x86_64
```

**Note:** the specified operating system kit must be installed prior to
running `create-software-profile`.

When creating software profiles to represent cloud-based nodes, the
argument `--no-os-media-required` can be used to avoid the need to
install OS installation media:

``` {.shell}
create-software-profile --name Compute --no-os-media-required
```

The `--no-os-media-required` argument is **only** effective when
provisioning cloud-based compute nodes, which have an operating system
image defined and a pre-existing operating system installation.

##### Creating from JSON software profile template

Dump an existing software profile to a JSON file:

``` {.shell}
get-software-profile --name execd --json >mytemplate.json
```

Use the template to create new software profile(s):

``` {.shell}
create-software-profile --name newexecd --template mytemplate.json
```

**Hint:** use `--name` when creating from the template to override the
software profile name defined in the template.

#### Updating software profiles

To modify a software profile, use `update-software-profile`. Most fields
can be updated, but things set during provisioning (such as the OS,
kernel, name format, or disk partitioning) will only affect *future*
nodes, not *existing* nodes. Software packages are updated on all
existing nodes the next time the cluster is updated.

Software profiles can be edited using the following command:

``` {.shell}
update-software-profile --name <NAME> ...
```

**Note:** it is not possible to change the operating system of an
existing software profile.

The `schedule-update` command will then synchronize the cluster.

##### Locked state

Software profiles can be *optionally* locked to disallow adding or
removing nodes. This feature is useful for applications where only a
fixed set of nodes is supported.

The default lock state of a newly created software profile is
"Unlocked".

Set the locked state to "SoftLocked" with the following command:

``` {.shell}
update-software-profile --name NAME --soft-locked
```

This will "soft lock" the software profile such that nodes cannot be
added and/or removed without the use of the `--force` argument specified
to `add-nodes` or `delete-node`, respectively.

Use `update-software-profile --name NAME --hard-locked` to "hard lock"
the software profile which prevents all `add-nodes` or `delete-node`
operations, regardless of the usage of the `--force` flag. In order to
add or delete nodes from a hard locked software profile, it is necessary
to first revert the lock to "soft locked" or disable it entirely.

Clear (or remove) any software profile lock with the following command:

``` {.shell}
update-software-profile --name NAME --unlock
```

##### Software profile minimum and maximum nodes

Software profiles do not have imposed minimums but will by default not
allow for more than a maximum of 25 nodes.

The following command imposes a software profile minimum:

``` {.shell}
update-software-profile --name NAME --min-nodes 16
```

When a minimum is applied, nodes in the specified software profile
cannot be deleted without using the `--force` argument. This is
irrespective of any software profile locks.

Conversely, it is also possible to impose a maximum number of nodes
within a software profile:

``` {.shell}
update-software-profile --name NAME --max-nodes 16
```

Any requests to add additional nodes beyond the imposed maximum of 16
will be rejected.

Clear minimum or maximum limits by specifying `none` as the argument to
`--min-nodes` or `--max-nodes` respectively:

``` {.shell}
update-software-profile --name NAME --min-nodes none
```

``` {.shell}
update-software-profile --name NAME --max-nodes none
```

``` {.shell}
update-software-profile --name NAME --min-nodes none --max-nodes none
```

Having no maximum implies that an unlimited number of nodes can be
created for a software profile. **Use this setting with caution,
especially when using automation rules for scaling up clusters.** If you
have no maximum set and your scaling rules have a bug, you could end-up
with an (unintentionally) very high bill for cloud services.

#### Deleting software profiles

Software profiles can be deleted using the `delete-software-profile`
command. Software profiles with associated nodes cannot be deleted until
the nodes are first deleted. In addition, hypervisor software profiles
cannot be deleted if they are referenced in an existing hardware
profile.

Example:

``` {.shell}
delete-software-profile --name Compute
```

### Hardware and software profile mapping

Hardware and software profiles must be *mapped*, or associated,
together.

For example, this prevents addition of non-functioning nodes. As an
example, it would prevent attempting to install a hypervisor onto a
virtual node.

The Tortuga administrator can create mappings using the command:

``` {.shell}
set-profile-mapping --hardware-profile <HWPROFILE> \
    --software-profile <SWPROFILE>
```

Hardware and software profiles are unmapped using the
`delete-profile-mapping` command.

### Kits and Components

#### Kits and Components Overview

A *kit* is the Tortuga packaging format for applications that will be
installed and managed by Tortuga.

Some kits include applications that extend the capabilities of Tortuga,
such as adding support for cloud providers and/or hypervisors. These
kits are commonly called *resource adapter kits*. Other kits include
application software, such as Univa Grid Engine.

Tortuga itself automatically installs a kit called the `base` software
kit. This kit contains *components* that are fundamental to the core
operation of Tortuga. Components contained within this kit can be
enabled on the installer node to configure additional Tortuga
functionality.

Kits distributed are as bzip2 compressed archive files.

The kit filename has the following format:

``` {.shell}
kit-<name>-<version>-<iteration>.tar.bz2
```

### Display list of installed kits

The `get-kit-list` command will display all installed kits (application
+ operating system):

``` {.shell}
[root@tortuga ~]# get-kit-list
awsadapter-7.0.3-0
base-7.0.3-0
centos-7.0-0
ganglia-3.7.2-1
gceadapter-7.0.3-0
simple_policy_engine-7.0.3-0
snmp-7.0.3-0
uge-8.6.4-0
```

To display operating system kits only, use the `--os` argument:

``` {.shell}
get-kit-list --os
```

#### Installing kits

Kits are installed using the following command:

``` {.shell}
install-kit kit-sample-1.0-0.tar.bz2
```

#### Components

Kits contain one or more *components*. Components are logical "packages"
providing the Puppet recipes and integration logic needed to use the
software in the kit.

For basic kits (ie. resource adapter), a single component may be
sufficient. More complex kits include multiple components, especially
when an application includes client and server functionality.

See the kit documentation for details on what components it provides,
what those components do, and how to configure them.

### Display all installed components

Use `get-component-list` to display all available components.

``` {.shell}
[root@tortuga ~]# get-component-list
snmp-7.0.3-0 snmpd-7.0.3
base-7.0.3-0 core-7.0.3
base-7.0.3-0 installer-7.0.3
base-7.0.3-0 dhcpd-7.0.3
base-7.0.3-0 dns-7.0.3
awsadapter-7.0.3-0 management-7.0.3
gceadapter-7.0.3-0 management-7.0.3
uge-8.6.4-0 qmaster-8.6.4
uge-8.6.4-0 execd-8.6.4
simple_policy_engine-7.0.3-0 engine-7.0.3
ganglia-3.7.2-1 gmetad-3.7.2
ganglia-3.7.2-1 gmond-3.7.2
centos-7.0-0 centos-7.0-x86_64-7.0.3
```

#### Display list of enabled components

Using the argument `--software-profile` or `-p` (shortcut to
`--software-profile Installer`), the list of components enabled on the
specified software profile will be displayed.

For example, to display the components enabled on the Tortuga installer:

``` {.shell}
[root@tortuga ~]# get-component-list --software-profile Installer
base-7.0.3-0 installer-7.0.3
base-7.0.3-0 dns-7.0.3
uge-8.6.4-0 qmaster-8.6.4
```

or using the shortcut:

``` {.shell}
get-component-list -p
```

To display the components enabled on software profile "Compute":

``` {.shell}
get-component-list --software-profile Compute
```

#### Enabling Components

Components are enabled per software profile using the `enable-component`
command. For example, to enable the `pdsh` component on the Tortuga
installer:

``` {.shell}
enable-component -p base-7.0.3-0 pdsh-7.0.3
```

**Hint:** Since it is unlikely to be another component named "pdsh", use
the command-line shortcut:

``` {.shell}
enable-component -p pdsh
```

Components are disabled using the `disable-component` command.

**Note:** due to the nature of uninstalling software from existing
compute nodes, it is **highly recommended** to reinstall/reprovision
compute nodes after changing the enabled components.

The `schedule-update` command must be used after components have been
enabled/disable to synchronize the cluster. See the "Cluster
Synchronization" section.

#### Removing Kits

Kits are removed using the `delete-kit` command. A kit may not be
deleted if any of its components are enabled on a software profile. The
'base' and 'clonezilla' kits may not be deleted at all.

``` {.shell}
delete-kit --name badkit --version 7.0 --iteration 0
```

**Never** attempt to delete a kit if a component was enabled or
disabled, and the cluster is currently being synchronized. Doing so will
lead to unpredictable results.

#### Cluster synchronization

Whenever a hardware or software profile is changed, the changes are made
to the information stored in the Tortuga database. These changes will
take effect on any future nodes added to the cluster. In many cases,
however, the changes include software (re)configurations which must be
applied to existing nodes in the cluster as well.

Any pending changes can be pushed to the cluster using the
`schedule-update` command. This command triggers the Puppet agents on
nodes in the cluster to configure the nodes as specified by their
profiles, including any changes that need to be made.

Puppet performs updates asynchronously in the background and as such,
does not guarantee a specific completion time. The amount of time needed
depends on the number of nodes affected, and the scope of the changes.

#### Base Kit

The "base" kit is a special kit which is included automatically when you
install Tortuga. It contains components to manage built-in Tortuga
features.

##### Internal use base components

The following components in the base kit are internally used by Tortuga
and should never be explicitly enabled or disabled:

-   `core`
-   `installer`

##### Base component: dhcpd

The `dhcpd` component can be enabled only on the `Installer` software
profile.

If enabled, the installer node will configure and manage a DHCP server
running on any "provisioning" networks defined in Tortuga.

This component must be enabled to provision *local* (non-cloud) nodes.

Enable the `dhcpd` component with the command:

``` {.shell}
enable-component -p base-7.0.3-0 dhcpd-7.0.3
```

`/opt/puppetlabs/bin/puppet agent --onetime --no-daemonize` is used to
synchronize only the Tortuga installer. `schedule-update` could also be
used (as described above), however since this component is only
applicable to the installer node, it is unnecessary to schedule an
entire cluster update.

##### Base component: dns

The `dns` component provides domain name services (DNS) for nodes
managed/provisioned by Tortuga. It is necessary to enable this component
for most installation types.

**Note:** The `dns` component can be enabled only on the `Installer`
software profile.

When enabled, the Tortuga installer node will automatically set up and
configure a DNS server that has a mapping entry for every node in the
system to its associated IP address.

Enable the `dns` component with the command:

``` {.shell}
enable-component -p base-7.0.3-0 dns-7.0.3
```

###### Configuring Tortuga private DNS domain

The global Tortuga private DNS domain is used when Tortuga generates a
compute node host name when provisioning on-premise physical or virtual
machines or when *optionally* enabled in resource adapter(s) using the
`override_dns_domain` resource adapter configuration setting.

On Tortuga 7.0.3 (and later), the `set-private-dns-zone` command-line is
used to display the current "private" DNS zone by calling it without an
argument:

``` {.shell}
[root@tortuga ~]# set-private-dns-zone
cloud.univa.com
```

On Tortuga versions prior to 7.0.3, use `ucparam` to get the current
(private) DNS domain. The Tortuga default private DNS domain is
`private`.

``` {.shell}
[root@tortuga ~]# ucparam get DNSZone
cloud.univa.com
```

Use `set-private-dns-zone <DOMAIN>` to set (private) DNS domain. For
example:

``` {.shell}
set-private-dns-zone cloud.mydomain.com
```

**Note:** do not use `ucparam set` to set the privte DNS domain as this
does not perform all of the necessary configuration to apply the change
in Tortuga.

###### DNS Configuration: Dnsmasq

The Tortuga-managed
[Dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html "Dnsmasq")
service is configured through the template file
`$TORTUGA_ROOT/config/dnsmasq.conf.tmpl`.

If the template file does not exist, Tortuga will automatically create a
barebones configuration file, which is automatically written to
`/etc/dnsmasq.conf`.

A sample
[Dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html "Dnsmasq")
template file exists in
`$TORTUGA_ROOT/config/dnsmasq.conf.tmpl.example`, which is very similar
to the boilerplate template used in the absence of this file.

Do **not** modify `/etc/dnsmasq.conf` directly as it will be overwritten
by Tortuga.

Any modifications made to the
[Dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html "Dnsmasq")
configuration template must be reflected in the Tortuga system by
running `genconfig dns` (as `root`) on the Tortuga installer. Restart
the [Dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html "Dnsmasq")
service as follows:

RHEL/CentOS 6:

``` {.shell}
service dnsmasq restart
```

RHEL/CentOS 7:

``` {.shell}
systemctl restart dnsmasq
```

Consult
[Dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html "Dnsmasq")
documentation for further configuration details.

##### Base component: pdsh

The `pdsh` component can be enabled on the `Installer` software profile.
If enabled, the `pdsh` (Parallel Distributed Shell) command will be
installed. This command is used by Tortuga when managing non-virtual
nodes to reboot nodes, but is also available for generic use.

Normally this component must be enabled to provision physical nodes. It
is not necessary to enable this component if the `pdsh` program is
already in the system `PATH` for every compute node.

### Users

Although Tortuga must be installed as the `root` user, and Tortuga
commands will work when run as the root user, it may not always be
desirable to do this for security reasons. Tortuga supports
Tortuga-specific users so non-system accounts can run commands. Tortuga
users *are not the same as system users*, and different system users are
not prohibited from using the same Tortuga username/password.

The Tortuga administrative user is created during Tortuga setup. Tortuga
commands run by the `root` Linux user are considered to be run by this
administrative user without requiring that a username or password be
specified.

The commands `add-admin`, `delete-admin`, `get-admin`, `get-admin-list`,
and `update-admin` manage Tortuga-specific users. Compute nodes in the
cluster are accessed "normally" using the standard access method(s) for
their operating systems.

The commands `add-admin-to-profile` and `delete-admin-from-profile` set
the hardware and/or software profiles to which a user has access. Other
than the main Tortuga administrative user, users should only be granted
access to the profiles they will use.

### Configuring Tortuga for provisioning

Tortuga can *provision* operating system software on a node. Nodes are
booted (be they bare metal/physical nodes which are powered on, or
virtual machine nodes which are allocated and started on a hypervisor),
and Tortuga detects them through a DHCP request, then assigns an IP
address and boots the OS installer remotely.

The OS installer runs in unattended mode, reboots the machine once the
OS is installed. After first boot, Puppet installs any software defined
by the software profile of the node.

Before this can happen, however, Tortuga needs to copy the necessary
files to boot and install the OS.

By default, the default Kickstart file tempate assigns a random `root`
password to all compute nodes for security purposes.

Networking Requirements
-----------------------

Tortuga requires a private network for provisioning. This network will
be managed by the installer node. This network does not require Internet
access, and may be implemented with a VLAN.

Example 1: The installer has two NICs: `eth0` and `eth1`. The `eth0`
interface is connected to the 'public' network. The `eth1` interface is
connected only to the systems in the datacenter as nodes and
hypervisors, and carries the provisioning network.

Example 2: The installer has a single NIC, `eth0`. The `eth0` interface
is connected to the 'public' network. An `eth0.10` sub-interface is
defined in the OS for use as a tagged VLAN, and the switch port is set
to allow tagged traffic for VLAN 10. The `eth0` interfaces of the
systems in the datacenter serving as nodes and hypervisors are connected
to ports on the switch set to place all untagged traffic on VLAN 10.

### Adding the Provisioning NIC

Provisioning network(s) are registered with Tortuga using the `add-nic`
utility. For example:

``` {.shell}
add-nic --nic <interface>
```

A typical dual-homed Tortuga installer may have the private/provisioning
network connected to the `eth1` device. The follow command-line would be
used to register the private/provisioning network:

``` {.shell}
add-nic --nic eth1
```

If the interface is associated with a VLAN (in this example, VLAN ID
100), the command-line would be as follows:

``` {.shell}
add-nic --nic eth1.100
```

**Hint:** `add-nic --autodetect` to get a list of detected network
interfaces on the Tortuga installer node.

Tortuga automatically obtains networking information based on the
network interface you select. The networking configuration of the
specified network interface can also be manually overridden. See
`add-nic` command usage (`add-nic --help`) for more information.

*Important firewall note:* If a firewall is running on the Tortuga
installer, please see the section "Firewall Configuration" under
"Planning for Installation" to verify proper configuration. Incorrect
firewall configurations will cause provisioning failures.

#### Multiple Provisioning NICs

Tortuga supports multiple private/provisioning network subnets.

For example, if `eth1` and `eth2` on the Tortuga installer were
connected to private/provisioning network subnets, the provisioning NICs
would be added successively as follows:

``` {.shell}
add-nic --nic=eth1
add-nic --nic=eth2
```

When multiple provisioning networks are used, it is necessary to
configure Tortuga to uniquely identify the provisioning subnets.

Add the following to the `[dns]` section in the DNS component
configuration file (`$TORTUGA_ROOT/config/base/dns-component.conf`):

``` {.shell}
[dns]
...
enable_interface_aliases = True
...
```

This will configure the Tortuga DNS host name assignment such that the
Tortuga installer has a unique identifier on each private/provisioning
subnet.

**Note:** if adding a second provisioning NIC with existing compute
nodes, the existing compute nodes will need to be refreshed. Run
`schedule-update` to synchronize DNS changes.

Enabling Tortuga Components for Provisioning
--------------------------------------------

Enable the following base components on the installer for provisioning:

-   `dhcpd`
    -   Enables ISC DHCP daemon on provisioning network
-   `dns`
    -   Enables DNS services on provisioning network
-   `pdsh` (*optional*)
    -   Parallel distributed shell for performing batch operations on
        many nodes

These components are enabled using `enable-component`. For example:

``` {.shell}
enable-component -p base-7.0.3-0 dhcpd-7.0.3
enable-component -p base-7.0.3-0 dns-7.0.3
```

Use `get-component-list` to see the exact name of the components and
versions.

Before synchronizing the cluster, it might be desirable to change
component configuration. Refer to section on DNS configuration prior to
completing the cluster synchronization.

`schedule-update` must be run after enabling components to synchronize
the installer configuration.

### Package-based Node Provisioning

#### Installing an OS Kit

An OS "kit" is a special kind of software kit. Instead of an archive
file, it is installed using the installation CD/DVD of an operating
system. The only component of an OS kit is the OS itself, and this
component cannot be enabled or disabled on any profile, and is treated
as a special case, referenced in the hardware and sometimes software
profile of a node.

You *must* install an OS kit in order to provision compute nodes.

To install an OS kit, use the `install-os-kit` command. This command has
several special flags:

-   `--media` -- specifies the location of the OS media, which should be
    the location of the installation DVDs for that OS; see below for
    supported types
-   `--symlinks` -- specifies that symbolic links should be used instead
    of copying files, to save space

The media accepted includes file directories, such as the mount point of
a physical DVD or copy of all its files, the name of an ISO file (which
will have its contents copied), or a web-based repository of the format
`http://<repositorylocation>/`. You can use multiple media by separating
them with a comma, as in `--media /media/disk1,/media/disk2`.

Symbolic linking is supported only for directories, and not ISOs or web
repositories. Tortuga *does not verify or check* that the files are
always available after a reboot, so this option should only be used if
you have a permanent copy of the files on the local system, or you
automatically mount it upon every reboot. If these files are not present
when you attempt to provision a node, it will fail and your only
indication will be at the node's attached terminal screen.

The files copied when you install an OS kit are placed into the depot
directory, selected during installation, defaulting to
`/opt/tortuga/depot`.

Note that symbolic linking is supported only for directories, where the
files are always available. You cannot symlink an ISO or proxied
location.

##### Installing OS kit Examples

Install (proxy) OS media through a mirror:

``` {.shell}
install-os-kit --mirror --media http://<CentOS mirror URL>/centos-6.4-x86_64/
```

If using this method of installing OS media, it is *highly recommended*
that the URL is for a host on your local network due to performance
reasons. Specifying a remote URL, for example that of a "true" CentOS
mirror, will result in much slower compute node provisioning time.

Install OS media from locally mounted media:

``` {.shell}
install-os-kit --media /media/disc1,/media/disc2
```

This copies the contents of the OS media found in subdirectories
`/media/disc1` and `/media/disc2` into Tortuga.

Install (symlink) OS media from locally mounted media:

``` {.shell}
install-os-kit --media /media/disc1,/media/disc2 --symlinks
```

Note: this requires that the media is *always* available at the
specified paths.

Install OS media from ISOs:

``` {.shell}
install-os-kit --media /isos/centos1.iso,/isos/centos2.iso
```

#### Kickstart configuration variable expansion

As an example, the `$timezone` variable in the default `kickstart.tmpl`
is set using `ucparam` as follows:

``` {.shell}
ucparam set Timezone_zone <TZSPEC>
```

where `<TZSPEC>` is the exact time zone specification as output by
`timedatectl list-timezones`. For example,

``` {.shell}
ucparam set Timezone_zone America/New_York
```

Please note, the Tortuga configuration setting `Timezone_utc` is not
currently used in the default Kickstarte template file. Set this
manually in the Kickstart file template as appropriate.

Use `ucparam list` to display list of Tortuga configuration settings.

Special Configurations
----------------------

After completing the steps in this section, you may in some cases need
to change the provisioning network parameters. You can view the network
using the `get-network-list` command. You can modify the network using
`update-network`.

Some important items to note about the provisioning network:

The `--start-ip` option can be used to change the lowest (start) IP
address that will be given out via DHCP. This is useful if you have
pre-allocated and placed systems on the provisioning network which will
*not* be managed or known to Tortuga. For example to change the start IP
of the network 10.2.0.0/255.255.255.0 to 10.2.0.3, the following command
can be used:

``` {.shell}
update-network --network 10.2.0.0/255.255.255.0 --start-ip 10.2.0.3
```

The `--increment` option allows you to reserve multiple IP addresses for
each node which is provisioned, if needed:

``` {.shell}
update-network --network 10.2.0.0/255.255.255.0 --increment 2
```

Nodes provisioned will be assigned every other IP addresses.

It is unnecessary to set the VLAN options or DHCP/static options in the
provisioning network when following the configuration actions described
earlier in this section.

### Setting up NAT for Tortuga compute nodes

Use the following commands to enable IP forwarding through the Tortuga
installer along with network address translation (NAT) for the compute
nodes:

### Enable IP forwarding on the Tortuga installer

``` {.shell}
echo 1 > /proc/sys/net/ipv4/ip_forward
```

### Enable NAT

In this example, it is assumed `eth0` on the Tortuga installer is
connected to the "public" network and `eth1` is the private or
provisioning network.

``` {.shell}
/sbin/iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
/sbin/iptables -A FORWARD -i eth0 -o eth1 -m state \
    --state RELATED,ESTABLISHED -j ACCEPT
/sbin/iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
```

Managing Clusters
-----------------

Managing a cluster in Tortuga essentially means just a few things. Nodes
can be added and removed, and configured (as well as transitioned
between configurations).

### Adding Nodes

Nodes are added to a Tortuga cluster using the `add-nodes` command.

The `add-nodes` command has the basic syntax:

``` {.shell}
add-nodes --count <NUMBER> --hardware-profile XXXX --software-profile YYYY
```

where `XXXX` is the name of an existing hardware profile and `YYYY` is
the name of an existing software profile.

The `add-nodes` command operates asynchronously. When `add-nodes` is
run, it will return immediately after validating the request. Use the
CLI `get-node-requests` to check on status of node requests.

#### Adding physical nodes or virtual machines by MAC address

Use the `--mac-addr` argument to `add-nodes` when adding physical
(on-premise) nodes for PXE booting and Anaconda installation.

For example:

``` {.shell}
add-nodes --mac-addr AA:BB:CC:DD:EE:FF \
    --software-profile XXXX --hardware-profile YYYY
```

This command will add a node entry for an on-premise node and allow that
node to be provisioned accordingly.

#### Manually adding a node

To add a node not provisioned by Tortuga, but may be managed (such as a
node which is a pre-installed hypervisor), use the following syntax:

``` {.shell}
add-nodes --hardware-porofile XXXX --software-profile YYYY \
    --host-name <HOSTNAME> [--mac-addr <MAC ADDRESS> \
    --ip-address <IP ADDRESS>]
```

If a node to be added is *not* on the provisioning network, the hardware
profile (see the associated section) *must* have it's location set to
`remote`, or Tortuga will attempt to reserve an IP address on the
provisioning network and use it for the node.

Nodes added in this manner do not automatically update their status. Use
the `update-node-status --status Installed` command to mark a node added
in this manner as ready for use.

### Reboot and/or reinstalling nodes

Existing nodes can be rebooted using the `reboot-node` command-line
interface.

For example:

``` {.shell}
reboot-node --node <nodespec>
```

The `--reinstall` option added to the `reboot-node` command-line will
force a reinstallation (where it makes sense; for example, on physical
nodes). When supported by the resource adapter, nodes will be
automatically reset to initiate the reprovisioning.

``` {.shell}
reboot-node --node <nodespec> --reinstall
```

### Deleting nodes

Nodes are deleted using the `delete-node --node <nodespec>` command. The
"nodespec" parameter may be a comma-separated list of nodes, and may
include wildcards. The asterisk (\*) wildcard must be quoted to avoid
shell interpretation, but a percentage sign (%) may be used as an
alternative without the need for escaping/quoting.

The `--force` flag may be useful to delete nodes which are in a state
other than *Installed*. In some situations, however, node deletion will
be blocked. For example, a hypervisor node may not be deleted while
hosting other nodes.

Example:

Delete node named "compute-01":

``` {.shell}
delete-node compute-01
```

Delete all nodes matching the wildcard \"compute\*\":

``` {.shell}
delete-node "compute*"
```

**Note:** wildcard spec must be escaped (or quoted) for use in `bash`.

As with `add-nodes`, `delete-node` also runs asynchronously and will
return immediately after it is run. Use the CLI `get-node-requests` to
check the status of a `delete-node` request.

### Idling and activating nodes

**Note:** this is a deprecated feature and is only supported by
on-premises compute nodes.

An "idle" node is one that is known by Tortuga but is currently
inactive. This state may be useful if the software associated with a
given profile uses an expensive license, and that license must be freed.

Idled nodes are reinstalled/reprovisioned once (re)activated. Copy any
important data from the local disk before idling.

For example, to idle the node "compute-01.private":

``` {.shell}
idle-node --node compute-01.private
```

To activate an idled node and bring it back to the installed state, use
the command
`activate-node --node <nodespec> --software-profile <SWP NAME>`. The
software profile must be specified as part of the activation sequence
because the node does not retain a history of previous software profiles
used.

For example, to reactivate the idle node "compute-01.private" in the
software profile Compute:

``` {.shell}
activate-node --node compute-01.private --software-profile Compute
```

(Re)activating a node requires a reprovision, and will take the same
amount of time as provisioning the node initially.

#### Idle/activate semantics

Node idle/activate semantics vary across resource adapters and are
typically useful only for Tortuga hybrid cluster installations.

For example, for Amazon EC2-based compute nodes within a Tortuga hybrid
cluster, idle nodes maintain presence in Tortuga, however have no
"backing" instance in Amazon EC2.

Idle/activate on VMware vSphere simply means stopping a virtual machine
(for idle), and (re)starting that VM (for activate).

Idle/activate semantics *do not* apply to physical nodes.

### Shutting down and Starting up Nodes

The `shutdown-node` command will issue an OS shutdown command via the
resource adapter.

This is useful for nodes which should no longer be running at all, but
should remain "known" to the cluster.

For example, to shutdown the node "vm-01":

``` {.shell}
shutdown-node --node vm-01
```

*Note:* shutting down a physical node will turn off the power, requiring
either remote power capabilities or a visit to the physical location to
restore power at a later time.

The `startup-node --node <nodespec>` command will start a node which was
previously shut down. In most cases, this is useful for virtual nodes in
a local cloud. The `--destination` option can be used, if supported, to
select a hypervisor to run the virtual node.

### Transferring nodes between software profiles

**Note:** this is a deprecated feature for on-premises nodes only!

Any node, regardless of whether it is physical or virtual, may have its
software profile changed using the `transfer-node` CLI. This command
will re-provision (as necessary) the node to bring into compliance with
the new software profile.

Transfer node (in *Installed* state) to new software profile:

``` {.shell}
transfer-node --node <node name> --software-profile <dest software profile>
```

For example, to transfer 1 node:

``` {.shell}
transfer-node --count 1 --software-profile <dest software profile>
```

**Note:** the "destination" software profile must already have been
mapped to use the node's hardware profile.

Transfer 6 nodes from source software profile:

``` {.shell}
transfer-node --count 6 --src-software-profile execd \
    --software-profile Compute
```

Tortuga does its best to make an intelligent determination of which
nodes to transfer, favoring idle and unused nodes when possible.

### Node states

The output of `get-node-status` can reveal nodes in Tortuga can exist in
one of several different states:

  -----------------------------------------------------------------------
  State                               Description
  ----------------------------------- -----------------------------------
  Installed                           Node is available and ready to use.

  Provisioned                         Node has been added to Tortuga and
                                      is in the process of being
                                      bootstrapped. Nodes in the
                                      'Provisioned' state should
                                      successfully transition to
                                      'Installed' state.

  Expired                             Existing node is being reinstalled.
                                      Only nodes that have been idled and
                                      (re)activated or reinstalled will
                                      ever be in this state.

  Deleted                             Tortuga is in the process of
                                      removing this node. The backing
                                      instance has been
                                      terminated/destroyed and database
                                      cleanup will eventually remove the
                                      node record entirely.

  Error                               Consult `/var/log/tortugawsd` (or
                                      `get-node-requests`) to determine
                                      the cause of the node error state.

  Launching                           Tortuga has received and begun
                                      processing the add nodes request.
                                      This state is typically associated
                                      with cloud-backed node instances
                                      where there is a delay caused by
                                      the cloud platform.

  Allocated                           Tortuga has created node record(s)
                                      and is in the process of launching
                                      the backing instance.
  -----------------------------------------------------------------------

### Resource tagging

Tortuga supports resource (nodes, software profiles, and hardware
profiles) tagging, similar to what is offered by cloud providers.

#### Tagging operations

##### Add resource tag

Add node tag:

``` {.shell}
uc-tag add --node <node name> --tag <key>=<value>
```

Add software profile tag:

``` {.shell}
uc-tag add --software-profile <swprofile name> --tag <key>=<value>
```

Add hardware profile tag:

``` {.shell}
uc-tag add --hardware-profile <hwprofile name> --tag <key>=<value>
```

##### Remove tag from resource

Remove tag from node:

``` {.shell}
uc-tag remove --node <node name> --tag <key>
```

Remove tag from software profile:

``` {.shell}
uc-tag remove --software-profile <swprofile name> --tag <key>
```

Remove tag from hardware profile:

``` {.shell}
uc-tag remove --hardware-profile <hwprofile name> --tag <key>
```

##### Delete (unregister) tag

The `uc-tag delete` command removes (unregisters) tag and removes it
from all resources.

``` {.shell}
uc-tag delete --force --tag <key>
```

##### List all tags/values

``` {.shell}
uc-tag list
```

#### Querying resources by tag

##### Nodes

``` {.shell}
get-node-status --tag <key>
```

``` {.shell}
get-node-list --tag <key>
```

##### Tagging Software profiles

``` {.shell}
get-software-profile-list --tag <key>
```

##### Tagging Hardware profiles

``` {.shell}
get-hardware-profile-list --tag <key>
```

Advanced Topics
---------------

### "Off-line" installation

The process for installing Tortuga in an environment that is entirely
off-line is completed in two steps. The first step is to download the
installation dependencies on a host that does have internet access.

#### Prepare Off-line Installation Dependencies

The script `prep-offline-install.sh` is to be run on an internet
connected host; one that has unrestricted access to package repositories
required by the Tortuga installer. This includes `yum.puppetlabs.com`,
the EPEL repository, and sites redirected from PyPI (the Python Package
Index).

##### Run `prep-offline-install.sh` script

Depending on bandwidth, this will take a few seconds to a few minutes.
The total dependencies downloaded are approximately 150MB.

The files will be downloaded to a subdirectory named `tortuga-deps` in
the local directory.

**Note:** some (most?) warnings/errors displayed during execution of
`prep-offline-install.sh` can be safely ignored.

##### Create tar from artifacts

This step is not necessary, however it makes it easier to move the
dependencies to the \"disconnected' Tortuga server as a single file.

``` {.shell}
tar czf tortuga-deps.tar.gz tortuga-deps/
```

##### Copy dependencies tarball

Copy the dependencies tarball `tortuga-deps.tar.gz` to the server where
Tortuga is to be installed.

#### Tortuga Installation

The Tortuga installation on the "disconnected" server must reference the
previously downloaded dependencies.

##### Prerequisites

It is *assumed* that the RHEL/CentOS repository will be available for
the Tortuga installation process. Alternatively, this can be substituted
for a locally available media ISO, mounted on `/media/cdrom`, and with
the `c7-media` YUM repository enabled.

Compute nodes require access to the same RHEL/CentOS repository. Refer
to the section *Configuring OS distribution proxy* below for more
details.

##### Extract dependencies tarball

Extract the dependencies tarball from the previous step.

``` {.shell}
tar zxf tortuga-deps.tar.gz -C /tmp
```

This command will create the directory `/tmp/tortuga-deps`.

##### Installing Tortuga using local dependencies

Run the Tortuga installation script `install-tortuga.sh` with the
`--dependencies-dir` argument, otherwise it will use the internet to
download dependencies.

``` {.shell}
install-tortuga.sh --dependencies-dir=/tmp/tortuga-deps ...
```

Once installed, `/opt/tortuga/bin/tortuga-setup` can be run as normal
after running `install-tortuga.sh`.

Provisioned compute nodes are automatically configured to use the local
installation dependencies, instead of connecting to remote sites.

#### Configuring OS distribution proxy

It is necessary to set up access to OS distribution YUM repositories in
an environment where Tortuga compute nodes do not have direct access to
upstream OS distribution YUM repositories.

By default, the Tortuga off-line installation sets up a YUM repository
under `$TORTUGA_ROOT/www_int/compute-os-repo`.

There are three options for making the OS distribution repository
available to the compute nodes.

**Note:** only one of the following mechanisms is required.

##### 1. Locally hosted OS distribution repository

The following steps will serve the OS distribution repository from the
Tortuga installer:

-   Remove the default directory as set up by Tortuga

    ``` {.shell}
    rm -rf $TORTUGA_ROOT/www_int/compute-os-repo
    ```

-   Copy or loopback mount the distribution ISO locally

    The goal here is making the OS distribution repository available in
    a well-known location within the Tortuga environment.

    -   Copy contents of OS distribution ISO to
        `$TORTUGA_ROOT/www_int/compute-os-repo`

        ``` {.shell}
        rsync -av /media/cdrom/ $TORTUGA_ROOT/www_int/compute-os-repo
        ```

    or:

    -   Loopback mount OS distribution ISO into local filesystem on
        Tortuga installer.

        ``` {.shell}
        mount -ro loop <distribution ISO> $TORTUGA_ROOT/www_int/compute-os-repo
        ```

        This will serve the contents of the specified OS distribution
        ISO in a common location under the Tortuga internal web server
        accessible to compute nodes.

##### 2. Proxying to an external OS distribution repository

Configure Squid (or other proxy) to proxy to an upstream OS repository
and modify the offline bootstrap script (ie.
`$TORTUGA_ROOT/config/aws-bootstrap-offline.tmpl`) to use that proxied
path.

Refer to the documentation of the proxy for details on how to proxy a
specific host/path.

The filename of this repository is
`/etc/yum.repos.d/tortuga-offline-centos.repo` as set up by the default
off-line bootstrap script. Modify the value of `baseurl` to point to the
proxied URL on the Tortuga installer.\`

##### 3. Install OS distribution "kit" using Tortuga

Install the desired OS distribution using `install-os-kit`. This will
automatically configure the repository on Tortuga compute nodes.

#### Resource adapter bootstrap script

The AWS resource adapter includes a bootstrap script
`aws-bootstrap-offline.tmpl` which configures the offline dependencies
and OS repositories. It is *expected* that the end-user will need to
modify this for their particular environment.

Use
`adapter-mgmt update -r AWS -p Default -s user_data_script_template=aws-bootstrap-offline.tmpl`
to enable this for offline compute nodes in the AWS environment. Other
resource adapters/cloud providers will require similar configuration.

### Compute Node Proxy Support

It is possible to define proxy settings for use by compute nodes in
environments where there is no direct connectivity between the Tortuga
installer and compute nodes.

The proxy is configured through the Puppet Hiera mechanism and is
applied directly to software profiles and the nodes contained therein.

#### Setting up a proxy server

Tortuga proxy support was tested exclusively with the [Squid caching
proxy](http://www.squid-cache.org), though others are equally as capable
and suitable.

The default Squid configuration needs *minor* modification to tunnel SSL
ports `8443/tcp` (Tortuga webservice) and `8140/tcp` (Puppet server).

The installation of a proxy server within the Tortuga environment can be
automated using the built-in Puppet server. See the section
*Puppet-based Configuration Management* in this manual.

#### Tortuga proxy settings

The following proxy settings are available:

-   `tortuga::config::puppet_proxy_http_host`
-   `tortuga::config::puppet_proxy_http_port`
-   `tortuga::config::puppet_proxy_http_user` (*optional*)
-   `tortuga::config::puppet_proxy_http_password` (*optional*)
-   `tortuga::config::proxy_uri`
-   `tortuga::config::proxy_user` (*optional*)
-   `tortuga::config::proxy_password` (*optional*)

The settings with the `puppet_` prefix apply specifically to the Puppet
client run on the compute nodes. The settings with the `proxy_` prefix
apply to both the YUM repository URLs used by the compute nodes as well
as accessing the Tortuga webservice and internal HTTP server.

#### Example Proxy configuration

For example, to apply these settings to the "Compute" software profile,
add the proxy configuration to
`/etc/puppetlabs/code/environments/production/data/tortuga-Compute.yaml`.

**Note:** the file name `tortuga-Compute.yaml` is case-sensitive and
**must** match the software profile name exactly.

Port 3128 is the default port used by the Squid proxy. If using an
alternate proxy, this value is likely to be different.

``` {.yaml}
---
version: 5

tortuga::config::puppet_proxy_http_host: myproxy
tortuga::config::puppet_proxy_http_port: 3128

tortuga::config::proxy_uri: http://myproxy:3128
```

**Note:** it is currently necessary to duplicate the proxy host/port/uri
settings as seen above. The Puppet proxy settings require a host name
only for the value of `tortuga::config::puppet_proxy_http_host`.
Specifying a URL here is incorrect and will not work.

The proxy configuration takes effect immediately. If the setting(s) are
changed after an existing node deployment, run `schedule-update` to
trigger a system-wide change, otherwise invoke a Puppet update on each
affected compute node, as necessary.

### Managing Operating System Updates

#### Red Hat Enterprise Linux

As Red Hat Enterprise Linux (RHEL) is a commercially licensed operating
system, access to the OS media and patches is done through the
subcription service. This requires that all RHEL nodes in Tortuga must
be properly licensed and registered with RHEL, either by proxy to a
site-local license server or to Red Hat itself.

Aside from configuring the Tortuga installer for compute node access to
the external network, nothing special needs to be done to manage
operating system updates.

#### CentOS

When compute nodes are provisioned by Tortuga, they are provisioned
using the OS media provided by `install-os-kit`.

For most users, this would be the downloadable DVD OS media for major
release versions of CentOS.

Between each major release, the CentOS team releases update packages
available from the 'updates' repository. It is these updated packages
that present an issue.

As part of the Tortuga installation procedure, the installer downloads
and caches dependent packages later required when provisioning compute
nodes. This includes packages such as Puppet, MCollective, and their
dependencies. These packages are subsequently dependent on core OS
packages (ie. python-devel, ruby, and others). Therein lies the
"problem"- if the patchlevel of the OS on the installer is different
than that of the OS media, the cached packages will have dependencies on
OS packages newer than what is available on the OS media.

There are three viable solutions or workarounds for this issue:

1.  no patches
2.  automatic patches through connected compute node
3.  manually managed patches

**Hint:** Custom Puppet modules associated with compute software
profiles and/or custom repositories added to the default Kickstart file
template are useful for managing YUM repositories for compute nodes. The
built-in Apache HTTP Server on the Tortuga installer can also be used to
host package updates.

##### Scenario 1: No patches

The Tortuga installer is fixed at the patchlevel of the OS media used to
provision compute nodes.

For example, if the installer is running CentOS 7.4, it stays at CentOS
7.4 for its lifetime. In other words, the 'updates' repository (defined
in '/etc/yum.repos.d/CentOS-Base.repo') must be disabled.

**Note: No patched packages can be installed on the installer prior to
installation of Tortuga!**

All compute nodes will be provisioned from the CentOS 7.4 OS media as
supplied by the administrator.

Pros:

-   simplest configuration

Cons:

-   no OS patches. This is *not recommended* for Internet connected
    nodes or outward facing nodes
-   may present issues for certain applications requiring OS patches

##### Scenario 2: Automatic patches through connected compute nodes

This scenario follows the default CentOS updates repository strategy.

When dealing with compute nodes on a Tortuga provisioning network, it is
easily possible to grant them external access by using network address
translation (NAT) as built into the Linux kernel.

See the section below on setting up NAT on the Tortuga installer to
enable external network access from Tortuga compute nodes.

Pros:

-   all OS patches, including security patches, are available to all
    nodes in the cluster

Cons:

-   compute nodes require access to 'updates' package repository

#### Scenario 3: Manually managed patches

When a compute node is provisioned by Tortuga, it installs the base
operating system from the OS media as provided by 'install-os-kit'.
Packages which constitute the Tortuga "base" kit are installed from
'/opt/tortuga/depot/kits/base/7.0.3-0/noarch'.

Updated packages can be dropped into this directory and will be
automatically available to Tortuga provisioned compute nodes.

**Note: after updating packages in
`/opt/tortuga/depot/kits/base/7.0.3-0/noarch`, it is required to run
`createrepo` to update the Tortuga **base\*\* kit YUM repository
metadata.\*\*

The key packages are `puppet-*`, `mcollective-*`, and the `ruby`
dependencies.

Pros:

-   flexibility

Cons:

-   manual package dependency management

### Puppet & MCollective

Tortuga uses
[MCollective](https://puppet.com/mcollective/ "MCollective") to trigger
Puppet runs using the MCollective `puppet` plugin from the Tortuga
installer node.

The end-user can manually trigger [Puppet](http://puppet.com "Puppet")
runs using the MCollective command `mco puppet ...`. For example, the
following command will trigger a Puppet run on the node
"`compute-01.private`":

``` {.shell}
mco puppet runonce -I compute-01.private
```

Multiple nodes can be specified:

``` {.shell}
mco puppet runonce -I compute-01.private -I compute-02.private
```

If the `-I` argument is excluded, the Puppet will be run on all Tortuga
managed nodes. This is the command the Tortuga CLI `schedule-update`
calls.

It is also possible to do basic troubleshooting using the MCollective
`ping` plugin:

``` {.shell}
mco ping
```

Sample output from the `mco ping` command on a 5 node cluster:

``` {.shell}
[root@tortuga ~]# mco ping
compute-03.private                       time=131.10 ms
compute-01.private                       time=132.27 ms
compute-02.private                       time=133.54 ms
compute-04.private                       time=140.16 ms
tortuga.private                         time=163.66 ms


--- ping statistics ---
5 replies max: 163.66 min: 131.10 avg: 140.14
```

If a Tortuga node does not respond to ping or is not displayed in this
list, it is not being recognized by Puppet and/or Tortuga.

Consult the Puppet Labs [MCollective
documentation](https://docs.puppet.com/mcollective) for further
information about MCollective and other potential use cases.

### Tortuga Puppet Integration & Extensibility

#### Puppet-based Configuration Management

##### Overview

Configuration management of nodes within Tortuga is done entirely via
Puppet. By using the Tortuga Puppet integration, it is very easy to
include end-user supplied Puppet modules to configure Tortuga managed
compute nodes.

The [Puppet Documentation Index](https://docs.puppet.com/puppet/) is the
definitive resource for all things Puppet. In particular, the [Type
Reference](https://docs.puppet.com/puppet/latest/type.html) and
[Language
Reference](https://docs.puppet.com/puppet/latest/lang_summary.html).

##### Integrating external/third-party Puppet modules

Third-party and/or in-house Puppet modules can be easily integrated
within Tortuga environment using the Puppet
[Hiera](https://docs.puppet.com/hiera/ "Hiera") functionality.
Third-party modules for many different applications and system
configurations can be found at [Puppet
Forge](https://forge.puppet.com/ "Puppet Forge").

##### Create a custom/site-specific Puppet module

The Puppet command-line interface includes functionality to generate a
boilerplate Puppet module framework using the `puppet module generate`
command as follows:

``` {.shell}
puppet module generate --skip-interview mycompany/mymodule
```

This generates a Puppet module named "mymodule" in a subdirectory named
`mymodule` in the current working directory.

Make modifications to `mymodule/manifests/init.pp` (such as examples
from below).

Compile this module using `puppet module build mymodule` and install it
as follows:

``` {.shell}
puppet module install mymodule/pkg/mycompany-mymodule-0.1.0.tar.gz
```

The Puppet module "mymodule" can now be used in the context of Tortuga.

**Note:** any modifications to the module "source" code must be compiled
and installed. If the module already exists, add the `--force` flag to
the `puppet module install` command-line as follows:

``` {.shell}
puppet module install --force mymodule/pkg/mycompany-mymodule-0.1.0.tar.gz
```

##### Adding Puppet module to all Tortuga-managed resources

To apply a Puppet module to all Tortuga-managed resources, including the
Tortuga installer, edit the file
`/etc/puppetlabs/code/environments/production/data/tortuga-extra.yaml`
and define the `classes` value as follows:

``` {.yaml}
---
version: 5

classes:
  - <Puppet module/class name>
```

or using the example module `mymodule` from above:

``` {.yaml}
---
version: 5

classes:
  - mymodule
```

This will cause the module `mymodule` to apply to all nodes in the
Tortuga environment, including the Tortuga installer.

##### Adding Puppet module to specific software profile

Create a YAML file
`/etc/puppetlabs/code/environments/production/data/tortuga-<NAME>.yaml`,
where "NAME" is the software profile name where the Puppet
module/classes are to be applied. Please note, this filename is case
sensitive.

For example, to add the module "docker" to the software profile "execd",
create a file named
`/etc/puppetlabs/code/environments/%{environment}/data/tortuga-execd.yaml`.
The contents of this standard YAML formatted file would appear as
follows:

**Note:** this assumes the Puppet module module is previously installed.
Modify `metadata.json` in your custom Puppet module to add a dependency
on the "docker" module to have it automatically installed when
"mymodule" is installed.

``` {.yaml}
---
version: 5

classes:
  - docker
```

or using the `mymodule` example above:

``` {.yaml}
---
version: 5

classes:
  - mymodule
```

`mymodule` would only apply to nodes in the software profile "execd".

#### Simple Puppet Recipes

The examples below are simplistic in nature, however having many Puppet
type references configuring many applications and/or configuration files
or users/groups will result in a large amount of code. Refer to the
Puppet "[Language:
Basics](https://docs.puppet.com/puppet/latest/lang_summary.html)" guide
for further information on creating Puppet classes, organizing Puppet
files/modules/classes, and general tips on coding for Puppet in an
efficient and maintainable manner.

Using the `mymodule` example from previous, this code could be pasted
into `mymodule/manifests/init.pp` to be applied to the configured nodes
(either all nodes, or only the software profile for which the module was
enabled).

##### Managing `/etc/hosts`

Puppet includes the `host` resource for managing the `/etc/hosts` file.

In this very basic example, an `/etc/hosts` entry for the host
`myhost.example.com` is created and associated with the IP address
`1.2.3.4`

``` {.puppet}
host { 'myhost.example.com':
    ensure       => present,
    host_aliases => [
        'myhost',
    ],
    ip           => '1.2.3.4',
}
```

##### User Account Management

If creating an environment where each node will have users/groups
managed manually (ie. with the assistance of a directory service like
NIS or LDAP), the following code can be used:

``` {.puppet}
group { 'engineers':
    gid => 1234,
}

group { 'sales':
    gid => 1240,
}

group { 'other':
    gid => 1250,
}

user { 'tom':
    uid        => 2001,
    group      => 'engineers',
    managehome => true,
    require    => Group['engineers'],
}

user { 'dick':
    uid        => 2002,
    group      => 'engineers',
    managehome => true,
    require    => Group['engineers'],
}

user { 'harry':
    uid        => 2003,
    group      => ['sales', 'other'],
    managehome => true,
    require    => [
        Group['sales'],
        Group['other'],
    ],
}
```

This code can be inserted into the example module verbatim, however it
is recommended to structure the code into separate classes for ease of
maintainability. For example, define all the groups in one class, define
all the users in another class, and make a dependency chain between
them.

For example, modify `mymodule/manifests/init.pp` as follows:

``` {.puppet}
class mymodule {
  contain mymodule::groups
  contain mymodule::users
}

class mymodule::groups {
   # TODO: do group stuff here
}

class mymodule::users {
  require mymodule::groups

  # TODO: do user stuff here knowing that 'mymodule::group' has already
  # been applied.
}
```

##### Managing Services

If the service is already known to the system (ie. `systemctl` or
`chkconfig --list` shows the service), it can be managed by the
following:

``` {.puppet}
service { 'myservicename':
    ensure => running,
    enable => true,
}
```

##### Package Management

Package repositories can be added using the `yumrepo` type:

``` {.puppet}
yumrepo { 'my_yum_repo':
    ensure        => present,
    baseurl       => 'http://url.to.yum.repo',
    descr         => 'This is my custom repository',
    enabled       => true,
    target        => 'myrepo.repo',
    repo_gpgcheck => false,
}
```

Packages can be added using the `package` type:

``` {.puppet}
package { 'mypackage':
    ensure => installed,
}
```

If installing from a custom repository, ensure the package resource has
a dependency on the module:

``` {.puppet}
package { 'custompkg':
    ...
    require => Yumrepo['customrepo'],
    ...
}
```

##### Mounting Volumes and Drives

###### NFS

``` {.puppet}
mount { '/my/local/mountpoint':
    ensure  => mounted,
    atboot  => true,
    dump    => 0,
    fstype  => 'nfs',
    options => 'defaults',
    device  => 'nfsserver:/exported/nfs/path',
}
```

###### Local Volumes

``` {.puppet}
mount { '/my/local/mountpoint':
    ensure  => mounted,
    atboot  => true,
    dump    => 0,
    fstype  => 'ext4',
    options => 'defaults',
    target  => '/dev/sdb1,
}
```

###### Other

Any filesystem or storage volume that cannot be mounted using the
standard Linux `mount` command must be handled differently. Other
volumes, such as Amazon S3, Amazon Glacier, etc., will need to be
mounted/made accessible using their native CLIs. These can be automated
using the Puppet `exec` type.

##### Calling arbitrary scripts and commands

Scripts and commands are called using the Puppet `exec` resource. A key
point here is that an `exec` will be called every time Puppet runs. This
can make it sometimes necessary to use "marker" files or check for the
existence of other files/directories to ensure the script isn't run
multiple times. Tortuga will run Puppet on all compute nodes for each
cluster to maintain coherency.

In this example, the script `/usr/local/bin/myscript.sh` is run, which
creates a file `/tmp/marker_file.txt`. Puppet is aware of this file
through the `creates` attribute and if this file exists on successive
runs, the script will *not* be run again.

``` {.puppet}
exec { '/usr/local/bin/myscript.sh':
    creates   => '/tmp/marker_file.txt',
    logoutput => true,
}
```

The attribute `logoutput` defaults to `onerror`, which means it will
only display output from the `exec` command if it returns a non-zero
return code. In the above example , the output of the `exec` command
will *always* be logged because it is set to `true`.

In this example, the arbitrary command `acommand` is executed only if
the file `/tmp/marker_file` does **not** exist. If the file does exist,
the command will not be run. Note that the `path` attribute is defined
in this example because the fully-qualfiied path to `acommand` was not
provided, nor was the path to `test`. Puppet will automatically search
the specified path for the commands `acommand` and `test`.

``` {.puppet}
exec { 'acommand':
    path   => ['/bin', '/usr/local/bin', '/usr/bin'],
    unless => 'test -f /tmp/marker_file.txt',
}
```

Applications can be installed from tarballs using `exec` resources. For
example:

``` {.puppet}
exec { 'tar zxf mytarball.tar.gz -C /opt/install_directory':
    path   => ['/bin', '/usr/bin', '/usr/local/bin'],
    unless => 'test -d /opt/install_directory',
}
```

The tarball `mytarball.tar.gz` will be extracted to
`/opt/install_directory` if that directory does not already exist. If
the tarball contains a top-level directory, the `unless` attribute can
be changed to properly test for its existence instead.

##### Using Third-Party Puppet modules

Third-party Puppet modules can be easily referenced from within the
example integration module as follows:

``` {.puppet}
class mymodule {
    ...
    include mysql::server
    ...
}
```

In this example, a reference is made to the `puppetlabs/mysql` module
(also used by Tortuga), which would cause `mysql-server` to be installed
on all nodes in the **Compute** software profile. This example assumes
the Puppet module has been previously installed.

Install third-party modules from [Puppet
Forge](https://forge.puppet.com/ "Puppet Forge") as follows:

``` {.shell}
puppet module install <modulename>
```

For example, to install the most popular "docker" module:

``` {.shell}
puppet module install garethr/docker
```

#### Other Configuration Management

Puppet includes several other types for performing configuration
management. The `augeas` type can be used to perform configuration tasks
for several common system configuration files. For example, those
contained within the `/etc/sysconfig` directory structure. It also is
capable of managing other application configuration files. Refer to the
[Augeas](http://augeas.net) website and documentation for a complete
list of applications and configuration files that can be configured
using Augeas.

For configuring applications that do not have a Puppet `type` or are not
supported by Augeas, a combination of `exec` resources can usually be
used to meet requirements.

#### Dependencies on Tortuga

It is sometimes necessary for Puppet recipes to be dependent on Tortuga
actions to ensure the sequence of events occurs in a logical manner. For
example, if using a Tortuga-based operating system package repository,
it is essential that this is configured prior to attempting to install
packages from it.

``` {.puppet}
class mymodule {
    # Ensure 'tortuga::packages' resource is "run" before this class
    require tortuga::packages

    ensure_packages(['vim-enhanced'], {'ensure' => 'installed'})
}
```

In the above example, the `require tortuga::packages` line would ensure
the Tortuga "tortuga::packages" class is "called" prior to the package
`vim-enhanced` is installed. In this particular instance, the Puppet
class "tortuga::packages" performs the initial configuration of YUM
package repositories on compute nodes.

For more information, consult the [Language: Relationships and
Ordering](http://docs.puppet.com/puppet/latest/reference/lang_relationships.html)
section of the Puppet documentation.

### Using Custom SSL Certificates

Tortuga uses a self-signed SSL certificate for securing web services.
This section explains how you can replace that self-signed certificate
with a custom third-party signed certificate.

It is assumed that you already have a SSL key, signed certificate, and a
CA certificate. If you need help using `openssl` for generating a CSR
(certificate signing request) to have signed by a CA (certificate
authority), there are many excellent resources online with detailed
explanations of the process.

The process of changing the SSL certificate is relatively simple. All it
involves is putting the correct files in the correct locations, and
restarting the affected services.

#### Files to Update

Place the certificate (or certificate chain) for your CA here:

``` {.shell}
/opt/tortuga/etc/CA/ca.pem
```

Put the key for your certificate here. Please note that it is important
than your key *not* be password protected:

``` {.shell}
/opt/tortuga/etc/certs/apache/server.key
```

Put your signed certificate here:

``` {.shell}
/opt/tortuga/etc/certs/apache/server.crt
```

Some services require the CA certificate chain and signed certificate to
be combined into a single file. It is important that the server
certificate come before the CA certificate chain in the file:

``` {.shell}
/opt/tortuga/etc/certs/apache/server-bundle.crt
```

The combined file described above can be created using the following
command:

``` {.shell}
cat /opt/tortuga/etc/certs/apache/server.crt \
    /opt/tortuga/etc/CA/ca.pem > /opt/tortuga/etc/certs/apache/server-bundle.crt
```

#### Restarting Services

Assuming the files in the previous section are in place, the following
services need to be restarted:

``` {.shell}
systemctl restart tortugawsd
systemctl restart celery
systemctl restart apache
```

Resource Adapters
-----------------

Resource adapters are the "connectors" between Tortuga and
virtualization and cloud platforms.

### Resource adapter configuration profiles

A resource adapter configuration profile contains resource adapter
settings, including access credentials, instance/VM types, compute node
operating system image, networking configuration, etc.

Tortuga supports multiple resource adapter configuration profiles to
allow custom tailored cloud provider configuration per groups of nodes.
The "Default" resource adapter configuration profile would usually
contain access credentials and default configuration. Resource adapter
configuration profiles can be created that only override or add specific
settings to eliminate the need for duplicating common settings.

A non-default resource adapter configuration profile can be set on
hardware profiles to automatically apply those settings to all nodes
added to that hardware profile.

Resource adapter configuration profiles can be created to support
multiple sets of access credentials to allow, for example, multiple UGE
clusters within a Tortuga managed environment, each with using a
different set of access credentials and therefore, billed to the
end-user independently.

#### Creating a resource adapter configuration profile

Create a resource adapter configuration profile named "example" for the
"AWS" resource adapter:

``` {.shell}
adapter-mgmt create --resource-adapter AWS --profile example \
    --setting key=value
```

**Hint:** `-r NAME` and `-p NAME` are shortcuts for
`--resource-adapter NAME` and `--profile NAME` arguments, respectively.

This command creates a resource adapter configuration profile named
"example" with one setting (*key=value*).

Using the `-A example` option when running `add-nodes` would instruct
Tortuga to obtain resource adapter configuration from this profile.

#### Setting default resource adapter configuration profile

Use the following command-line syntax to specify a default resource
adapter configuration profile:

``` {.shell}
update-hardware-profile --name aws \
    --default-resource-adapter-configuration-profile nondefault
```

**Hint:** use the `-A` shortcut instead of
`--default-resource-adapter-configuration-profile`

In this example, the default resource adapter configuration profile is
set to `nondefault` for the hardware profile `aws`. As described above,
the resource adapter configuration profile `nondefault` must be
previously created using `adapter-mgmt create -r XXX -p nondefault`.

Now when adding nodes using `add-nodes`, the resource adapter
configuration profile `nondefault` will be used for all nodes added to
the `aws` hardware profile.

It is also possible to specify `-A profilename` to override the default
resource adapter configuration profile:

``` {.shell}
add-nodes ... --hardware-profile aws -A otherprofile
```

Nodes added to the `aws` hardware profile will use the `otherprofile`
resource adapter configuration profile regardless of the default resoure
adapter configuration profile set on the hardware profile.

##### Importing an existing resource adapter configuration

For users of Tortuga versions prior to 7.0, the resource adapter
configuration was contained within a file. These existing resource
adapter configurations may be imported as follows:

``` {.shell}
adapter-mgmt import --resource-adapter AWS --adapter-config <filename>
```

This will create a `default` resource adapter configuration profile for
the specific resource adapter as well as individual configuration
profiles for all sections listed in the adapter configuration file.

#### List all resource adapter configuration profiles

For example, to list all resource adapter configuration profiles for the
"AWS" resource adapter, use the following command-line:

``` {.shell}
adapter-mgmt list --resource-adapter AWS
```

#### Show specific resource adapter configuration profile

To display all settings for a specific resource adapter configuration
profile:

``` {.shell}
adapter-mgmt show --resource-adapter AWS --profile default
```

All "secret" information (ie. AWS access/secret keys, passwords, etc.)
will be hidden from the output of `adapter-mgmt show` by default. To
display *all* information, add the `--all` argument. For example:

``` {.shell}
adapter-mgmt show --all --resource-adapter AWS --profile default
```

#### Deleting resource adapter configuration profiles

Delete the resource adapter configuration profile "example" from the
"AWS" resource adapter:

``` {.shell}
adapter-mgmt delete --resource-adapter AWS --profile example
```

#### Specify resource adapter configuration profile when adding nodes

Use `--resource-adapter-configuration-profile` (or its preferred
shortcut `-A`) to specify the resource adapter configuration profile
used when adding nodes:

``` {.shell}
add-nodes --count N \
    --hardware-profile aws --software-profile execd -A profilename
```

If the option `-A <profilename>` is provided, the specified resource
adapter configuration profile is used. If this profile does not exist,
an error will be displayed. If the profile specified does not contain
the full set of resource adapter configuration settings (ie.
credentials), the system will automatically use the "missing" values
from the `default` resource adapter configuration profile.

If the default resource adapter configuration profile is not set (as
described above), the `default` resource adapter configuration profile
is used.

**Note:** it is also possible to override the hardware profile default
resource adapter configuration using `--resource-adapter-configuration`
on the `add-nodes` command-line

Troubleshooting
---------------

### Troubleshooting Overview

Installation, configuration, and day-to-day operations in Tortuga
updates several log files, which can be used to identify Tortuga
failures or error conditions.

Due to the nature of some operations and external dependencies on
network services, for example, some failed operations cannot be logged
through the standard Tortuga logging mechanism. An example of this is
network traffic blocked by a firewall or misconfiguration in no network
connectivity, and others.

When such symptoms of "total failure" occur (i.e. nothing is working),
it is necessary to resort to primitive TCP/IP debugging procedures to
ensure basic connectivity.

### Log file formatting and convention

The log files are formatted with e date/time stamp, the log level (INFO,
ERROR, WARNING, TRACE), the process ID (pid) of the process that created
the log entry, and then the entry itself. All content after the pid is
free-form and may not conform to any one style suitable for parsing.

Commonly, DEBUG and TRACE messages will show the Python module name
before the operation. This also applies to log messages generated by the
resource adapters, with the difference being the resource adapter name
will appear in brackets before the log message.

### Installation and setup logging

There are several "stages" to a Tortuga installation. Each of these
installation and setup "stages" generates and/or updates log files.

The first stage is `install-tortuga.sh`, which is run after unarchiving
the distribution tarball. This operation creates and updates the log
file `/tmp/install-tortuga.log`.

The output contained in this log file is mostly from the commands run by
the `install-tortuga.sh` script. It is **not** a structured log file and
is mostly only useful if the initial installation process failed. This
file can be safely removed once installation is complete.

The next stage is setting up Tortuga after installation. Running
`tortuga-setup` to complete the installation process results in multiple
log files generated:

-   `/tmp/bootstrap.log` - output of the serverless Puppet bootstrapping
    process automatically run during the initial Tortuga setup.

-   `/tmp/tortuga_setup.log` - another Puppet run output to apply
    Tortuga installer changes made during the setup process.

The main Tortuga log file `/var/log/tortuga` is also created and updated
during the execution of `tortuga-setup`.

The creation of the Tortuga Certificate Authority (CA) generates two
files in `/tmp`:

-   `/tmp/tortuga-ca.log.*`
-   `/tmp/tortuga-server.log.*`

Other log files, such as those created/updated by
[ActiveMQ](http://activemq.apache.org/ "ActiveMQ"),
[MCollective](https://puppet.com/mcollective/ "MCollective"), [Apache
HTTP Server](https://httpd.apache.org), and
[MySQL](http://www.mysql.com) will also be created/updated during
Tortuga setup.

### Logging Configuration

The log level is configured through `$TORTUGA_ROOT/config/log.conf`.
This is a self-documented configuration file for the standard Python
**`logging`** facility used by Tortuga.

While it can be configured to redirect logging to different sinks,
change filename(s) of log files, etc, it is strongly recommended to
adjust nothing more than the log level unless comfortable with the
complexity of this configuration file.

Refer to the [Python
documentation](https://docs.python.org/release/2.6.6/library/logging.html)
for additional configuration information.

### Adjusting default log level

The current Tortuga distribution has DEBUG level logging enabled by
default. This causes additional logging, which can be useful during
initial installation and setup.

Note: changing to "trace" log level will result in much more logging and
may hinder Tortuga performance because of API level logging.

#### Comprehensive List of Log Files

-   `/tmp/install-tortuga.sh` (\*)
-   `/tmp/bootstrap.log` (\*)
-   `/tmp/tortuga_setup.log` (\*)
-   `/var/log/tortugawsd`
-   `/tmp/tortuga-ca.log.*` (\*)
-   `/tmp/tortuga-server.log.*` (\*)
-   `/var/log/httpd/tortugaint_{access,error}_log` (*Apache HTTP
    Server*)
-   `/var/log/httpd/tortugaws_{access,error}_log` (*Apache HTTP Server*)

\* denotes log files that are created once and never further updated.
They typically include raw command output and are strictly for debugging
purposes.

The following system log files will also contain output as a result of
Tortuga being installed and running:

-   `/var/log/messages`
-   `/var/log/activemq/*`
-   `/var/log/mcollective`
-   `/var/log/httpd/*`
-   `/var/log/mysqld.log`

### Troubleshooting failed Tortuga installation

There are several reasons why Tortuga may fail to install successfully:

1.  Intermittent networking

    Surprisingly, not all corporate LANs are created equally and
    intermittent networking may cause temporary outage and and Internet
    accessibility issues. The Tortuga installation process depends on
    reliable Internet access to retrieve package dependencies.

    If the Tortuga installation (`install-tortuga.sh`) succeeds, and the
    setup stage fails (`tortuga-setup`), it is possible to retry the
    setup simply by calling `tortuga-setup --force ...`.

    Consult log `/tmp/install-tortuga.sh` if the installation failure
    occurred during `install-tortuga.sh`, and logs `/tmp/bootstrap.log`,
    `/tmp/tortuga_setup.log` if the installation failure occurred during
    `tortuga-setup`.

2.  Lack of general Internet access

    Some sites do not permit open access to the Internet, which results
    in an immediate, failed Tortuga installation.

    The Tortuga installation procedure depends on unrestricted access to
    HTTP (port 80) and HTTPS (port 443) services on various remote sites
    to retrieve package dependencies. The installer does not explicitly
    disable proxies, and *should* adhere to any system-wide proxy
    settings.

    Please contact support\@univa.com for further support when
    installing Tortuga in an environment where Internet access is
    unavailable.

3.  Misconfigured/malfunctioning DNS

    The host name returned by the command `hostname --fqdn` must be a
    fully-qualified, DNS resolvable host name.

    This host name may be the host name of the public network interface
    (ie. interface connected to the corporate LAN) or the host name of
    the private network interface (ie. interface connected to
    private/provisioning network managed by Tortuga).

    Whatever the host name may be, the Tortuga installer **must** be
    able to resolve its own host name via DNS or `/etc/hosts`. Ensure
    the following `ping` command succeeds:

    ``` {.shell}
    ping -c5 `hostname --fqdn`
    ```

    During the installation process, Tortuga invokes Puppet to perform
    configuration management of the installer node. Part of the Puppet
    initial bootstrap process requires creating a certificate containing
    the fully-qualified domain name (FQDN) of the Tortuga installer
    node.

    It should be noted that, when enabled, Tortuga will also maintain
    its own DNS server (serving DNS requests to private/provisioning
    networks), however the initial Tortuga installation needs functional
    DNS to proceed. When all else fails, use `/etc/hosts` to add a
    static entry for the Tortuga installer host.

### Troubleshooting failed compute node provisioning

This section is mostly related to the provisioning of physical compute
nodes, as opposed to cloud-based compute nodes.

There is usually one cause for failed compute node provisioning and that
is network connectivity, or lack thereof.

1.  No (private) network connectivity

    Ensure the private/provisioning network interface on the Tortuga
    installer (*eth1*, for many) is connected to the same network as the
    proposed compute nodes. In demo/trial environments using virtual
    machines, this is usually as a result of the Tortuga installer VM
    not being connected to the same (virtual) network as the compute
    node VM(s).

    As suggested in the Quickstart section above, it is recommended when
    using Anaconda/Kickstart-based compute node provisioning, to set the
    root password of the compute node(s) to a known value. This will
    allow connecting to failed compute node installations that may be a
    result of misconfiguration of the Tortuga installer.

2.  Service (DHCP/DNS) conflicts on private network

    In some cases, when the private/provisioning network is being used
    for other nodes and/or services within a datacenter, this can result
    in DHCP/DNS services conflicting with those managed by Tortuga.

    A typical symptom here would be a compute node receving a DHCP
    address that is not the same as that assigned by Tortuga.

    Tortuga **cannot** function correctly in such an environment and
    must "own" exclusive access to the DHCP and DNS services on the
    private network it is managing.

Appendix A: Tortuga End-User License Agreement (EULA)
-----------------------------------------------------

Copyright 2008-2018 Univa Corporation

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Appendix C: Uninstalling Tortuga
--------------------------------

Tortuga itself is contained within the `/opt/tortuga` directory, however
there are configuration and support files elsewhere within the
filesystem.

**Note**: make a backup of of the entire filesystem prior to performing
these uninstallation steps!

If you are installing Tortuga 7.0 on top of an existing Tortuga 6.1.x
installation, the following operations should be performed on
RHEL/CentOS 7:

``` {.shell}
service sgemaster.tortuga stop
service activemq stop
systemctl stop httpd
systemctl stop mariadb
systemctl stop mcollective
systemctl stop tortugawsd
rm -f /etc/httpd/conf.d/{tortuga.conf,passenger.conf,puppetmaster.conf}
mv /opt/tortuga /opt/tortuga.orig
```

On RHEL/CentOS 6, substitute calls to `systemctl stop <name>` to
`service <name> stop`.
