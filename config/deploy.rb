default_run_options[:pty] = true
set :application, "sodalabs"
set :repository,  "ssh://67.23.35.50:8430/home/git/sodalabs"

# If you aren't deploying to /u/apps/#{application} on the target
# servers (which is the default), you can specify the actual location
# via the :deploy_to variable:
# set :deploy_to, "/var/www/#{application}"

# If you aren't using Subversion to manage your source code, specify
# your SCM below:
set :scm, :git
#set :scm_username, :git
set :scm_password, "t!m0r"
set :use_sudo, false
set :user, :sodalabs
set :runner, :sodalabs

set :media_root, "/u/media/#{application}/site_media"
set :template_root, "/u/media/#{application}/templates"

role :app, "67.23.35.50:8430"
role :web, "67.23.35.50:8430"
role :db,  "67.23.35.50:8430", :primary => true

set :media_root, "/u/media/#{application}/site_media"
set :template_root, "/u/media/#{application}/templates"
set :upload_root, "/u/media/#{application}/files"

namespace :deploy do
    [:start, :stop, :restart].each do |t|
        desc "#{t} django instances" 
        task t, :roles => :app, :except => { :no_release => true } do 
            run "supervisorctl #{t} sodalabs:*"
        end
    end

    task :migrate do 
        desc "Run manage.py syncdb"
        run "cd #{current_path}/#{application};python ./manage.py syncdb"
    end
    
    desc "[internal] create directories and add symlinks"
    task :finalize_update do
        # enforce production settings
        run "cp #{latest_release}/#{application}/production_settings.py #{latest_release}/#{application}/settings.py"
        
        # create symlink for shared blog_assets dir and logfile
        run <<-CMD
            rm -rf #{upload_root} &&
            ln -s #{shared_path}/files #{upload_root}
        CMD
        
        run "rm -rf #{media_root}"
        run "ln -s #{latest_release}/#{application}/media #{media_root}"
        run "rm -rf #{template_root}"
        run "ln -s #{latest_release}/#{application}/templates #{template_root}"

    end

end
