import cx_Freeze

executables = [cx_Freeze.Executable("nordvpn_checker.py")]

cx_Freeze.setup(
    name="NordVPN Checker",
    version="1.0",
    description="Check NordVPN accounts",
    executables=executables
)
