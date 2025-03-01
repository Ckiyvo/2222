import { createRouter, createWebHistory } from 'vue-router';
import ProjectManagement from '../components/ProjectManagement.vue'; // 根据实际路径调整
import ProjectDetail from '../components/ProjectDetail.vue'; // 根据实际路径调整

const routes = [
    {
        path: '/',
        name: 'ProjectManagement',
        component: ProjectManagement
    },
    {
        path: '/project/:projectName',
        name: 'ProjectDetail',
        component: ProjectDetail,
        props: true
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;