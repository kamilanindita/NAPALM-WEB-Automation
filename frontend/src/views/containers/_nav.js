export default [
  {
    _name: 'CSidebarNav',
    _children: [
      {
        _name: 'CSidebarNavItem',
        name: 'Dashboard',
        to: '/dashboard',
        icon: 'cil-speedometer',
      },
      {
        _name: 'CSidebarNavItem',
        name: 'Add Device',
        to: '/dashboard/add-device',
        icon: 'cil-library-add'
      },
      {
        _name: 'CSidebarNavItem',
        name: 'Device List',
        to: '/dashboard/device-list',
        icon: 'cil-list-rich'
      },
      {
        _name: 'CSidebarNavDropdown',
        name: 'ACL',
        icon: 'cil-terminal',
        items: [
          {
            name: 'ACL IPv4',
            to: '/dashboard/acl-ipv4'
          },
          {
            name: 'ACL IPv6',
            to: '/dashboard/acl-ipv6'
          }
        ]
      },
      {
        _name: 'CSidebarNavItem',
        name: 'Backup',
        to: '/dashboard/backup',
        icon: 'cil-cloud-download'
      },
      {
        _name: 'CSidebarNavItem',
        name: 'Restore',
        to: '/dashboard/restore',
        icon: 'cil-cloud-upload'
      },
      {
        _name: 'CSidebarNavItem',
        name: 'History',
        to: '/dashboard/history',
        icon: 'cil-history'
      },
    ]
  }
]