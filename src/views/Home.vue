<template>
<div id="home">
    <div class="title">HCIHUB</div>
    <el-autocomplete
      class="inline-input"
      v-model="state"
      :fetch-suggestions="querySearch"
      @select="toDetail()"
      @keyup.enter.native="toDetail()">
      <template slot-scope="{ item }">
        <div class="key-word">{{ item.value }}</div>
        <span class="conference">{{ item.conference }}</span>
      </template>
      <el-button slot="append" icon="el-icon-search" @click="toDetail()"></el-button>
    </el-autocomplete>
</div>
</template>
<script>
export default {
    data () {
        return {
            restaurants:[],
            state:''
        }
    },
    mounted() {
        this.restaurants = this.loadAll();
    },
    methods: {    
        querySearch(queryString, cb) {
            var restaurants = this.restaurants;
            var results = queryString ? restaurants.filter(this.createFilter(queryString)) : restaurants;
            // 调用 callback 返回建议列表的数据
            cb(results);
        },
        createFilter(queryString) {
            return (restaurant) => {
            return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0);
            };
        },
        loadAll() {
            return [
                { "value": "A", "conference": "IUI/2018/Ogata" },
                { "value": "B", "conference": "CHI/2018/Fekety" }
            ];
        },
        handleSelect(item) {
            console.log(item);
        },
        toDetail() {
            console.log(this.state)
            this.$router.push({
                path: '/detail?q='+this.state+''
            })
        }
    },
    created () {
    
    }
}
</script>

<style scoped>
#home {
    height: 100%;
    width: 100%;
    position: absolute;
    left: 0;
    /* background-color: rgb(0,98,132); */
    background-color: rgb(248,195,205);
    /* background-color: rgb(181,202,160); */
    /* background-color: rgb(134,166,151); */
    /* background-color: rgb(129,199,212); */
}
.title {
    font-size: 5.5vw;
    font-weight: bolder;
    color: rgb(173,35,51);
    margin-top: 15%;
}
.inline-input {
    display: block;
    width:30%;
    position: absolute;
    top:45%;
    left: 35%;
}
.el-input__inner {
   font-size: 1.5vw;
}
.el-input input {
    height:60px;
}
.key-word {
    text-overflow: ellipsis;
    overflow: hidden;
}
.conference {
    font-size: 12px;
    color: #b4b4b4;
}
</style>