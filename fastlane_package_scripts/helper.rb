#!/usr/bin/ruby

#require 'Plist'
#require 'xcodeproj'
require './ProjectConfig.rb'

def parseEnvironment(envArr)

  git_branch  = ENV['Git_Branch']
  testIn      = ENV['Environment_TestIn']
  testOut     = ENV['Environment_TestOut']
  preProduct  = ENV['Environment_PreProduct']
  custom_List = ENV['Environment_Custom_List']
  
  if testIn == "true"
    #内测环境 type = 1
    envArr.push({"name" => "TestIn", "type" => "1", "addr" => ""})
  end
  if testOut == "true"
    #外测环境 type = 2
    envArr.push({"name" => "TestOut", "type" => "2", "addr" => ""})
  end
  if preProduct == "true"
    #预发布环境 type = 3
    envArr.push({"name" => "PreProduct", "type" => "3", "addr" => ""})
  end

  #自定义环境 type = 4
  if !custom_List.nil? && !custom_List.empty?
    customArr = custom_List.split(/\n/)
    customArr.each do |environment|
      tempArr = environment.split(/=/)
      if tempArr.size == 2
         envArr.push({"name" => tempArr[0], "type" => "4", "addr" => tempArr[1]})
      end
    end
  end
end




def generate_ipa_name(scheme, env_name, cur_date, cur_time)
  
  packageName = scheme + "_" + cur_date + "_" + cur_time 
  packageName = packageName + "_" + env_name + ".ipa"
end








