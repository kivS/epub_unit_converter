<script>
import fileUploader from './components/file-uploader'

export default {
  name: 'app',
  components: {
    fileUploader
  }
}
</script>

<template>
  <div id="app">
    <file-uploader></file-uploader>
  </div>
</template>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
