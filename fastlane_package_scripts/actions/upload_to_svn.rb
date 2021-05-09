module Fastlane
  module Actions
    module SharedValues
      UPLOAD_TO_SVN_CUSTOM_VALUE = :UPLOAD_TO_SVN_CUSTOM_VALUE
    end

    class UploadToSvnAction < Action
      def self.run(params)

        ipa_path        = params[:package_Path]
        curSVNPath      = params[:remote_svn_path]
        local_svn_path  = params[:local_svn_path]


        #1 创建本次ipa的远端svn目录
        system "svn mkdir --parents #{curSVNPath} -m \"创建包目录\""

        #2 checkout刚刚创建的svn目录到本地
        system "svn checkout #{curSVNPath} #{local_svn_path}"

        #3 复制ipa包目录到本地svn目录
        system "cp -rf #{ipa_path} #{local_svn_path}"

        #4 svn提交
        system "cd #{local_svn_path} && svn add *  && svn commit -m \"提交测试包\""

      end


      #####################################################
      # @!group Documentation
      #####################################################

      def self.description
        "A short description with <= 80 characters of what this action does"
      end

      def self.details
        # Optional:
        # this is your chance to provide a more detailed description of this action
        "You can use this action to do cool things..."
      end

      def self.available_options
        # Define all options your action supports. 
        
        # Below a few examples
        [
          FastlaneCore::ConfigItem.new(key: :package_Path,
                                       env_name: "FL_UPLOAD_TO_SVN_Package_Path", # The name of the environment variable
                                       description: "Package Path for UploadToSvnAction", # a short description of this parameter
                                       ),
          FastlaneCore::ConfigItem.new(key: :remote_svn_path,
                                      env_name: "FL_UPLOAD_TO_SVN_Remote_SVN_Path", # The name of the environment variable
                                      description: "remote svn Path for UploadToSvnAction", # a short description of this parameter
                                      ),
          FastlaneCore::ConfigItem.new(key: :local_svn_path,
                                      env_name: "FL_UPLOAD_TO_SVN_Package_Path", # The name of the environment variable
                                      description: "local svn path for UploadToSvnAction", # a short description of this parameter
                                      )

        ]
      end

      def self.output
        # Define the shared values you are going to provide
        # Example
        [
          ['UPLOAD_TO_SVN_CUSTOM_VALUE', 'A description of what this value contains']
        ]
      end

      def self.return_value
        # If you method provides a return value, you can describe here what it does
      end

      def self.authors
        # So no one will ever forget your contribution to fastlane :) You are awesome btw!
        ["Your GitHub/Twitter Name"]
      end

      def self.is_supported?(platform)
        # you can do things like
        # 
        #  true
        # 
        #  platform == :ios
        # 
        #  [:ios, :mac].include?(platform)
        # 

        platform == :ios
      end
    end
  end
end
