import App from './App.svelte';

const app = new App({
    target: document.body,
    props: {
        api: '/api/'
    }
});

export default app;