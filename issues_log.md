# Log of issues faced during devleopment:

## venv environment:
During definitionof venv enivonment, could not avtivate it as i faced following issue:

```bash
.\activate : File D:\venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this 
system. For more information, see about_Execution_Policies at https:/go.microsoft.com/fwlink/?LinkID=135170.
```
This error is happening because PowerShell's execution policy is preventing you from running the Activate.ps1 script that sets up your virtual environment. This is a security feature in Windows.

This can be resolved by running following command with windows powershell as Administrator (as permanent solution)

```bash
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```