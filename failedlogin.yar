rule FailedLoginAdmin
{
    meta:
        description = "Detect failed login attempts for admin account"
        author = "Your Name"
        date = "2024-12-01"
    strings:
        $failed_login = "4625"
        $admin_account = "admin"
    condition:
        $failed_login and $admin_account
}
