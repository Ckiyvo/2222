<template>
  <div>
    <h2>项目管理</h2>
    <p>这是项目管理页面。</p>
    <!-- 创建页面按钮 -->
    <button @click="showCreatePageDialog = true">创建页面</button>
    <!-- 创建页面弹窗 -->
    <div v-if="showCreatePageDialog" class="create-page-dialog">
      <div class="dialog-content">
        <h3>创建页面</h3>
        <!-- 页面名称输入框 -->
        <input type="text" v-model="projectName" placeholder="项目名称">
        <!-- 上传文件模块 -->
        <div class="upload-button-module">
          <!-- 选择文件区域 -->
          <div class="upload-file-section" @click="openFileDialog('single')">
            <input
              type="file"
              ref="fileInputSingle"
              @change="handleFileChange('single')"
              multiple
              :accept="allowedFileTypes"
              style="display: none;"
            />
            <span>选择文件</span>
          </div>
          <!-- 选择文件夹区域 -->
          <div class="upload-folder-section" @click="openFileDialog('folder')">
            <input
              type="file"
              ref="fileInputFolder"
              @change="handleFileChange('folder')"
              multiple
              webkitdirectory
              directory
              style="display: none;"
            />
            <span>选择文件夹</span>
          </div>
        </div>
        <!-- 显示允许的文件类型 -->
        <p class="allowed-types">允许的文件类型: {{ allowedFileTypes.replace(/\./g, '').replace(/,/g, ', ') }}</p>
        <div v-if="selectedFiles.length > 0">
          <p>已选择文件: {{ selectedFiles.length === 1 ? selectedFiles[0].name : selectedFiles[0].name + ' 等 ' + selectedFiles.length + ' 个文件' }}</p>
        </div>
        <div v-if="invalidFiles.length > 0" style="color: red;">
          以下文件类型不允许上传: {{ invalidFiles.join(', ') }}
        </div>
        <!-- 创建和取消按钮 -->
        <button @click="createProject">创建</button>
        <button @click="showCreatePageDialog = false">取消</button>
      </div>
    </div>
    <!-- 项目列表 -->
    <div v-if="projects.length > 0">
      <h3>我的项目列表</h3>
      <div class="project-list">
        <div v-for="project in projects" :key="project.id" class="project-item" @click="goToProjectPage(project.name)">
          <p class="project-name">{{ project.name }}</p>
          <p class="project-time">{{ project.created_at }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRouter } from 'vue-router';

export default {
  name: 'ProjectManagement',
  data() {
    return {
      showCreatePageDialog: false,
      projectName: '',
      selectedFiles: [],
      invalidFiles: [],
      uploadUrl: 'http://127.0.0.1:8000/api/create_project/',
      getProjectsUrl: 'http://127.0.0.1:8000/api/get_projects/',
      allowedFileTypes: '.txt,.pdf,.doc,.docx,.csv,.jpg,.jpeg,.png,.wav,.mp3,.aac,.mp4',
      projects: []
    };
  },
  mounted() {
    this.getProjects();
  },
  methods: {
    createProject() {
      if (!this.projectName) {
        alert('项目名称不能为空');
        return;
      }
      if (this.invalidFiles.length > 0) {
        alert('存在不允许上传的文件类型，请重新选择。');
        return;
      }

      const formData = new FormData();
      formData.append('project_name', this.projectName);
      this.selectedFiles.forEach((file) => {
        formData.append('files', file);
      });

      axios.post(this.uploadUrl, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then((response) => {
        console.log('项目创建成功:', response.data);
        // 关闭弹窗
        this.showCreatePageDialog = false;
        // 清空输入框和文件列表
        this.projectName = '';
        this.selectedFiles = [];
        this.invalidFiles = [];
        // 刷新项目列表
        this.getProjects();
      })
      .catch((error) => {
        console.error('项目创建失败:', error);
        alert('项目创建失败，请稍后重试。');
      });
    },
    openFileDialog(type) {
      if (type === 'single') {
        this.$refs.fileInputSingle.click();
      } else {
        this.$refs.fileInputFolder.click();
      }
    },
    handleFileChange(type) {
      const inputRef = type === 'single' ? this.$refs.fileInputSingle : this.$refs.fileInputFolder;
      const files = inputRef.files;
      this.selectedFiles = [];
      this.invalidFiles = [];

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const fileExtension = file.name.split('.').pop().toLowerCase();
        if (this.allowedFileTypes.includes(`.${fileExtension}`)) {
          this.selectedFiles.push(file);
        } else {
          this.invalidFiles.push(file.name);
        }
      }
    },
    getProjects() {
      axios.get(this.getProjectsUrl)
      .then((response) => {
        this.projects = response.data.projects;
      })
      .catch((error) => {
        console.error('获取项目列表失败:', error);
      });
    },
    goToProjectPage(projectName) {
      const router = useRouter();
      router.push({ name: 'ProjectDetail', params: { projectName } });
    }
  }
};
</script>

<style scoped>
/* 弹窗样式 */
.create-page-dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.dialog-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
}

.dialog-content input {
  margin-bottom: 10px;
  padding: 5px;
}

.dialog-content button {
  margin: 5px;
}

.upload-button-module {
  display: flex;
  border: 1px solid #ccc;
  border-radius: 4px;
  overflow: hidden;
  cursor: pointer;
  margin-bottom: 10px;
}

.upload-file-section,
.upload-folder-section {
  flex: 1;
  padding: 20px;
  text-align: center;
  transition: background-color 0.3s ease;
}

.upload-file-section:hover,
.upload-folder-section:hover {
  background-color: #f0f0f0;
}

.upload-file-section {
  border-right: 1px solid #ccc;
}

.allowed-types {
  margin-bottom: 20px;
}

/* 项目列表容器 */
.project-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

/* 单个项目框 */
.project-item {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  width: calc(25% - 20px); /* 每行最多展示 4 个项目 */
  box-sizing: border-box;
  cursor: pointer;
}

/* 项目名称 */
.project-name {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
}

/* 项目创建时间 */
.project-time {
  font-size: 14px;
  color: #666;
}
</style>