#!/bin/bash

# 命令使用
# modulecreater XXXView

# 1.添加Pod到 项目的 Podfile文件中。
module_name=$1
addlib="pod '$module_name', :path => 'Pods/$module_name'"
python pod_target_add.py ../../XXXProject/Podfile cymini_pods "$addlib"

# 2.cd到项目的 Pods目录下
cd ../../XXXProject/Pods

# 3.创建XXX.podspec文件，并修改podspec文件
mkdir -p $module_name
cd $module_name
pod spec create $module_name

# 替换默认 podsepc 文件
python ../../../assetsTools/PodModule/replace.py $module_name.podspec "MIT \(example\)" "MIT"
python ../../../assetsTools/PodModule/replace.py $module_name.podspec ":git => \"http://EXAMPLE/$module_name.git\"" ":git => \"\""
python ../../../assetsTools/PodModule/replace.py $module_name.podspec "<<-DESC" "\"$module_name\""
python ../../../assetsTools/PodModule/replace.py $module_name.podspec "DESC" ""
python ../../../assetsTools/PodModule/replace.py $module_name.podspec "# spec.public_header_files = \"Classes/\*\*/\*.h\"" "spec.public_header_files = \"Classes/PublicHeader/**/*.h\""
python ../../../assetsTools/PodModule/replace.py $module_name.podspec "# spec.requires_arc = true" "spec.requires_arc = true"
python ../../../assetsTools/PodModule/replace.py $module_name.podspec "# spec.resource  = \"icon.png\"" "spec.resource_bundles = {\n    '$module_name' => ['Resources/*.xcassets'],\n  }"
python ../../../assetsTools/PodModule/replace.py $module_name.podspec "# spec.platform     = :ios, \"5.0\"" "spec.platform     = :ios, \"9.0\""


# 4.创建pod的 Classes/PublicHeader，Resources/Assets.xcassets目录， 
mkdir -p Classes
mkdir -p Resources

cd Classes
mkdir -p PublicHeader

# 公开头文件
echo -e "// " >> PublicHeader/${module_name}.h
echo -e "//  $module_name" >> PublicHeader/${module_name}.h
echo -e "//  ${module_name}.h" >> PublicHeader/${module_name}.h
echo -e "// \n" >> PublicHeader/${module_name}.h
echo -e "#import <Foundation/Foundation.h>" >> PublicHeader/${module_name}.h
echo -e "#import <UIKit/UIKit.h>\n" >> PublicHeader/${module_name}.h
echo -e "#ifndef ${module_name}_h" >> PublicHeader/${module_name}.h
echo -e "#define ${module_name}_h\n" >> PublicHeader/${module_name}.h
echo -e "static NSString * const ${module_name}_Version = @\"0.0.1\";\n" >> PublicHeader/${module_name}.h
echo -e "//#if __has_include(\"\")" >> PublicHeader/${module_name}.h
echo -e "//#import \"\"" >> PublicHeader/${module_name}.h
echo -e "//#endif\n" >> PublicHeader/${module_name}.h
echo -e "#endif /* ${module_name}_h */" >> PublicHeader/${module_name}.h

touch DeleteMe.m

cd ../Resources

mkdir -p Assets.xcassets

cd ../../../



# 5.回到工程根目录， 执行pod install安装该pod
pod install

# xed .