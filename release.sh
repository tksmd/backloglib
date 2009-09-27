#!/bin/bash
#
# Copyright 2009 Takashi SOMEDA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language
# governing permissions and limitations under the License.
#
# リリース作業用のシェル
# - svn のタグ付け
# - download 用アーカイブの作成
# - download 用アーカイブのアップロード
#
if [ $# -lt 1 ]; then
  echo "$0 <VERSION>"
  exit 1
fi
Version=$1

RepoBase="https://backloglib.googlecode.com/svn/"
TagBase="https://backloglib.googlecode.com/svn/tags/backloglib"
TrunkUrl="https://backloglib.googlecode.com/svn/trunk/backloglib"

if [ $(svn status . | wc -l) -gt 0 ]; then
  echo -n "modified items exist, continue ? [y|n] "
  while read ans
  do
    case ${ans} in
	    "y"|"Y")
	      echo "ok continue..."
	      break
	    ;;
	    "n"|"N")
	      exit 1
	    ;;
	    *)
	      echo "please answer y or n"
	    ;;
    esac 
  done
fi

# (1) タグ付け
TagUrl="${TagBase}/REL-${Version}"
svn ls ${TagUrl} > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "${TagUrl} already exists, please check your version"
  exit 1
fi
svn copy ${TrunkUrl} ${TagUrl} -m "[release.sh] add release tag ${Version}" 

# (2) アーカイブ作成
python setup.py sdist --force-manifest

# (3) アップロード
ArchiveFile="dist/backloglib-${Version}.tar.gz"
python googlecode_upload.py -s "backloglib release ${Version}" -p backloglib ${ArchiveFile}
