<template>
    <div>
        <h2>{{ projectName }} 项目详情</h2>
        <p>这是 {{ projectName }} 项目的详细信息页面。</p>
    </div>
</template>

<script>
export default {
    name: 'ProjectDetail',
    props: ['projectName']
};
</script>

<style scoped>
/* 可以添加项目详情页的样式 */
</style>