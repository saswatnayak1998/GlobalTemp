universe = vanilla
log = 7623db09eccee41830e4fab767e79c26.job.log
error = 7623db09eccee41830e4fab767e79c26.job.err
output = 7623db09eccee41830e4fab767e79c26.job.out

executable = submission_scripts/submit-7623db09eccee41830e4fab767e79c26.sh
arguments = 7623db09eccee41830e4fab767e79c26


should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = Anaconda3-2022.10-Linux-x86_64.sh, project.py, .signac, signac_project_document.json, workspace/7623db09eccee41830e4fab767e79c26, env.yml, submission_scripts/submit-7623db09eccee41830e4fab767e79c26.sh, espresso, scripts
transfer_output_files = 7623db09eccee41830e4fab767e79c26-signac_job_document.json, 7623db09eccee41830e4fab767e79c26-relax.md.out, 7623db09eccee41830e4fab767e79c26-relax.md.in, 7623db09eccee41830e4fab767e79c26-relax.md.temp

request_cpus = 4
request_memory = 100GB
request_disk = 100GB

queue 1