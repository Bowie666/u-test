pipeline {
    agent any

    stages {
        stage('1.pull code') {
            steps {
                git credentialsId: 'giteema', url: 'https://gitee.com/bowiehsu/u-test.git'
            }
        }
        stage('2.build code') {
            steps {
                sh '''echo "开始构建"
                    echo "构建完成"'''
            }
        }
        stage('3.deploy code') {
            steps {
                sshPublisher(publishers: [sshPublisherDesc(configName: '腾讯云', transfers: [sshTransfer(cleanRemote: false, excludes: '', execCommand: 'echo "传输成功"', execTimeout: 120000, flatten: false, makeEmptyDirs: false, noDefaultExcludes: false, patternSeparator: '[, ]+', remoteDirectory: 'func/', remoteDirectorySDF: false, removePrefix: '', sourceFiles: '*.en.md')], usePromotionTimestamp: false, useWorkspaceInPromotion: false, verbose: false)])
            }
        }
    }
}
