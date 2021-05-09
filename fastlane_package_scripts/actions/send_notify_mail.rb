
require 'viewpoint'
include Viewpoint::EWS

module Fastlane
  module Actions
    module SharedValues
      SEND_NOTIFY_MAIL_CUSTOM_VALUE = :SEND_NOTIFY_MAIL_CUSTOM_VALUE
    end

    class SendNotifyMailAction < Action
      def self.run(params)

        subject = "打包"
        content = "iOS端乾牛贷1.2.0版本目前接口联调已经​完毕,现正式提测。本次打包svn上传路径:" + params[:package_svn_path]
        
        recipientsArr = params[:recipients].split(/\n/)
        filterArr = Array.new()
        recipientsArr.each do |recipient|
          puts recipient
          if !recipient.empty? 
             filterArr.push(recipient)
          end
        end
        puts filterArr

        cli = Viewpoint::EWSClient.new params[:endpoint], params[:user], params[:password]
        cli.send_message subject: subject, body: content, to_recipients: filterArr


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

          FastlaneCore::ConfigItem.new(key: :endpoint,
                                       env_name: "FL_SEND_NOTIFY_MAIL_ENDPOINT", # The name of the environment variable
                                       description: "endpoint for SendNotifyMailAction", # a short description of this parameter
                                       ),

          FastlaneCore::ConfigItem.new(key: :user,
                                       env_name: "FL_SEND_NOTIFY_MAIL_USER", # The name of the environment variable
                                       description: "user for SendNotifyMailAction", # a short description of this parameter
                                       ),

          FastlaneCore::ConfigItem.new(key: :password,
                                       env_name: "FL_SEND_NOTIFY_MAIL_PASSWORD", # The name of the environment variable
                                       description: "password for SendNotifyMailAction", # a short description of this parameter
                                       ),

          FastlaneCore::ConfigItem.new(key: :recipients,
                                       env_name: "FL_SEND_NOTIFY_MAIL_RECIPIENTS", # The name of the environment variable
                                       description: "recipients for SendNotifyMailAction", # a short description of this parameter
                                       ),
          FastlaneCore::ConfigItem.new(key: :package_svn_path,
                                       env_name: "FL_SEND_NOTIFY_MAIL_PACKAGE_SVN_PATH", # The name of the environment variable
                                       description: "package svn path for SendNotifyMailAction", # a short description of this parameter
                                       )
        ]
      end

      def self.output
        # Define the shared values you are going to provide
        # Example
        [
          ['SEND_NOTIFY_MAIL_CUSTOM_VALUE', 'A description of what this value contains']
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
