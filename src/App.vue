<template>
  <div id="app">
    <!-- <div class="nav">
      <div class="nav-contain">
          <span class="home-link"><a href="/">HCIHUB</a></span>
      </div>
    </div> -->
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  /* font-family: PingFangSC-Regular, Microsoft Yahei, HeitiSC, Helvetica; */
  font-family: Helvetica Neue;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;
}
.nav {
  width: 100%;
  height: 6vw;
  position: fixed;
  top: 0;
  z-index: 100;
}
.nav-contain {
  list-style-type:none;
  width: 75%;
  text-align: left;
  margin: 0 auto;
  line-height: 6vw;
}
.home-link a {
  font-size: 3.5vw;
  font-weight: 900;                   
  text-decoration : none;
}
</style>
