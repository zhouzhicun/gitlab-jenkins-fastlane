module Fastlane
  module Actions
    module SharedValues
      MODIFY_ENVIRONMENT_CUSTOM_VALUE = :MODIFY_ENVIRONMENT_CUSTOM_VALUE
    end

    class ModifyEnvironmentAction < Action
      def self.run(params)

        env_Path            = params[:env_Path]
        env_Type_Pattern    = params[:env_Type_Pattern]
        env_Type            = params[:env_Type]
        env_Addr_Pattern    = params[:env_Addr_Pattern]
        env_Addr            = params[:env_Addr]

        puts env_Path
        puts env_Type_Pattern
        puts env_Type
        puts env_Addr_Pattern
        puts env_Addr

        #修改环境配置文件
        custom_env_pattern = "本机"
        recognized_custom_env_pattern = false

        lines = File.open(env_Path).readlines
        file = File.open(env_Path, "w")
        lines.each { 
          |cur_line| 

          #recognized_custom_env_pattern用来标志是否已匹配集群环境, 打包时所有自定义环境都配置在集群环境下。
          if cur_line[custom_env_pattern]
            recognized_custom_env_pattern = true
          end

          if cur_line[env_Type_Pattern] 
            #环境类型匹配成功
            file.puts("#{env_Type_Pattern} #{env_Type}")

          elsif !(env_Addr.empty?) && cur_line[env_Addr_Pattern] && recognized_custom_env_pattern
            
            #自定义环境匹配成功, 修改环境地址为当前地址, 再清除recognized_custom_env_pattern标志
            file.puts("#{env_Addr_Pattern} @\"#{env_Addr}\"")
            recognized_custom_env_pattern = false
          else
            #其他行原样输出
            file.puts(cur_line)  
          end
        }
        file.close


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
          FastlaneCore::ConfigItem.new(key: :env_Path,
                                       env_name: "FL_MODIFY_ENVIRONMENT_ENV_PATH", # The name of the environment variable
                                       description: "Environment path for ModifyEnvironmentAction", # a short description of this parameter
                                       ),

          FastlaneCore::ConfigItem.new(key: :env_Type_Pattern,
                                       env_name: "FL_MODIFY_ENVIRONMENT_ENV_TYPE_PATTERN", # The name of the environment variable
                                       description: "Environment type pattern for ModifyEnvironmentAction", # a short description of this parameter
                                       ),
          FastlaneCore::ConfigItem.new(key: :env_Type,
                                       env_name: "FL_MODIFY_ENVIRONMENT_ENV_TYPE", # The name of the environment variable
                                       description: "Environment Type for ModifyEnvironmentAction", # a short description of this parameter
                                       ),

          FastlaneCore::ConfigItem.new(key: :env_Addr_Pattern,
                                       env_name: "FL_MODIFY_ENVIRONMENT_ENV_ADDR_PATTERN", # The name of the environment variable
                                       description: "Environment addr pattern for ModifyEnvironmentAction", # a short description of this parameter
                                       ),
          FastlaneCore::ConfigItem.new(key: :env_Addr,
                                       env_name: "FL_MODIFY_ENVIRONMENT_ENV_ADDR",
                                       description: "Environment Address for ModifyEnvironmentAction",
                                       )
        ]
      end

      def self.output
        # Define the shared values you are going to provide
        # Example
        [
          ['MODIFY_ENVIRONMENT_CUSTOM_VALUE', 'A description of what this value contains']
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
