<template>
<div id="home">
    <div class="title"><span style="color:#4AA5E5">HCI</span><span style="color:#FCB75F">HUB</span></div>
    <div class="search-box">
        <input class="inline-input"
           v-model="state"
           @keyup.enter="toDetail()">
        <img src="../../static/search.png" @click="toDetail()">
    </div>
    
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
            return [];
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
    top: 0;
}
.title {
    font-size: 110px;
    font-weight: bolder;
    color: #000;
    margin-top: 15%;
    letter-spacing:10px;
}
.search-box {
    display: flex;
    width: 650px;
    height: 50px;
    padding:7px 10px;
    margin: 20px auto 0 auto;
    border: 1px solid #D8D8D8;
    border-radius: 20px;
}
.search-box input {
    width: 600px;
    height: 50px;
    outline: none;
    border: none;
    font-size: 25px;
}
.search-box img {
    width: 36px;
    height: 36px;
    padding: 7px 0;
}
/* .inline-input {
    display: block;
    width: 630px;
    margin: 0 auto;
}
.el-input {
    height: 60px!important;
}
.el-input__inner {
   font-size: 20px;
   height: 60px!important;
} */
/* .key-word {
    text-overflow: ellipsis;
    overflow: hidden;
}
.conference {
    font-size: 12px;
    color: #b4b4b4;
} */

</style>