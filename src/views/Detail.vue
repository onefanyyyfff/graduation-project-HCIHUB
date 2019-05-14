<template>
<div id="detail" v-loading="loading">
    <div class="top">
        <div class="top-content">
            <div class="logo" ref="logo">
                <a href="/">HCIHUB</a>
            </div>
            <div class="search">
                <!-- <el-input v-model="search" class="input-with-select" @keyup.enter.native="getNewList()"> -->
                <el-select v-model="timeValue" multiple placeholder="time" slot="prepend" style="width:120px;border:none" collapse-tags>
                    <el-option
                        v-for="(time,index) in times"
                        :key="index"
                        :label="time"
                        :value="time">
                    </el-option>
                </el-select>
                <input v-model="search" class="input-with-select" @keyup.enter.native="getNewList()">
                <img src="../../static/search.png">
                    <!-- <el-button slot="append" icon="el-icon-search"  @click="getNewList()"></el-button> -->
                <!-- </el-input> -->
            </div>
        </div>
    </div>
    <div class="sort-box">
        <span class="results">results:{{total}}</span>
        <span :class="{selectedType:sort===1,sortType:sort!==1}" @click="getNewSort(1)">RELAVANCE</span>
        <span :class="{selectedType:sort===2,sortType:sort!==2}" @click="getNewSort(2)">TIME</span>
    </div>
    <div class="bottom">
        <div class="bottom-content">
            <div class="select-opt">
                <div class="conf-title">
                    <span>SOURCES</span>
                </div>
                <div>
                    <el-checkbox-group v-model="selectConf" @change="getConfList" style="height:250px">
                        <el-checkbox v-for="(item,index) in ccfconferences" :key="index" :index="index" :label="item._id+':'+item.cnt"></el-checkbox>
                    </el-checkbox-group>
                </div>
                <div>
                    <div class="conf-subtitle" @click="more()">More</div>
                    <el-checkbox-group v-model="selectConf" @change="getConfList" v-if="showOtherConf">
                        <el-checkbox v-for="(item,index) in conferences" :key="index" :index="index" :label="item._id+':'+item.cnt"></el-checkbox>
                    </el-checkbox-group>
                </div>
            </div>
            <div class="result">
                <div v-for="(result,index) in results" :key="index" class="res-item">
                    <div class="title">
                        <a :href="result.url" class="title-link" target="_blank">{{pageNum+index}}.</a>
                        <a :href="result.url" class="title-link" target="_blank"><span v-html="result.title"></span></a>
                    </div>
                    <div class="detail-info">
                        <span>{{result.year}} </span>
                        <span>{{result.shortName}} </span>
                        <a v-for="(author,index) in result.authors" :key="index" :href="author.link" class="author-link" target="_blank">{{author.name}}</a>
                    </div>
                    <div class="notOpen" v-if="!result.openFlag" @click="showPieceFunc(result,index)">
                        <div>Summary:<span v-html="result.summary"></span></div>
                    </div>
                    <div class="summary-all" v-else @click="showPieceFunc(result,index)">
                        <div>Summary:<span v-html="result.summary"></span></div>
                    </div>
                </div>
                <div class="page">
                    <el-pagination
                        @current-change="handleCurrentChange"
                        :current-page.sync="currentPage"
                        layout="prev, pager, next"
                        :page-count="Math.ceil(total/10)">
                    </el-pagination>
                </div>
            </div>
        </div>  
        
        <div class="footer">
            <div class="footer-content">Copyright © 2017 清华大学 · 人机交互实验室 </div>
        </div> 
    </div>
</div>
</template>
<script>
import Vue from 'vue'
export default {
    data () {
        return {
            search:this.$route.query.q,
            timeValue:[],
            authorValue:[],
            times: [],
            authors:[],
            ccfconferences: [],
            conferences:[],
            results: [],
            currentPage: 1,
            pageSize:10,
            showPiece: [],
            selectConf: [],
            total: 0,
            showOtherConf: false,
            loading: true,
            pageNum: 1,
            sort: 1,
            screenWidth: document.body.clientWidth
        }
    },
    mounted () {
        if(this.screenWidth <500) {
            this.$refs.logo.hidden = true
        }
    },
    methods: {  
       more() {
            this.showOtherConf = ! this.showOtherConf
       }, 
       clear() {
           this.results = [],
            this.ccfconferences = [],
            this.conferences = [],
            this.times = [],
            this.authors = [],
            this.total = 0
       },
       showPieceFunc(result,index) {
            if(!result.openFlag) {
                Vue.set(result,'openFlag',true)
            }
            else {
                Vue.set(result,'openFlag',false)
            }
       },
       handleCurrentChange(val) {   
           this.loading = true               
           this.$http.post('http://39.105.69.251:8081/search_post/', {
                query:this.search,
                year: this.timeValue,
                authors: this.authorValue,
                conf: this.selectConf,
                index: val,
                sort: this.sort
            }).then(res => {
                this.loading = false
                this.results = res.body.result.reslist,
                this.currentPage = val;
                this.pageNum = (this.currentPage-1)*this.pageSize+1;
                window.scrollTo(0,0)
            })
       },
       getOriginList() {
            this.$http.post('http://39.105.69.251:8081/search_post/', {
                query:this.search,
                year: [],
                authors: [],
                conf: [],
                index: 1,
                sort: this.sort
            }).then(res => { 
                this.loading = false,
                this.currentPage = 1,  
                this.pageNum = 1,
                this.results = res.body.result.reslist,
                this.ccfconferences = res.body.result.ccf_confs,
                this.conferences = res.body.result.confs,
                this.times = res.body.result.years,
                this.authors = res.body.result.authors ,
                this.total = res.body.result.num
            })
        },
        getNewSort(sort) {
            this.loading = true 
            this.$http.post('http://39.105.69.251:8081/search_post/', {
                query:this.search,
                year: this.timeValue,
                authors: this.authorValue,
                conf: this.selectConf,
                index: 1,
                sort: sort
            }).then(res => { 
                this.loading = false,
                this.currentPage = 1,  
                this.pageNum = 1;
                this.results = res.body.result.reslist,
                this.sort = sort
            })
        },
        getNewList() {
            this.loading = true  
            this.clear()
            this.$http.post('http://39.105.69.251:8081/search_post/', {
                query:this.search,
                year: this.timeValue,
                authors: this.authorValue,
                conf: [],
                index: 1,
                sort: this.sort
            }).then(res => {
                this.loading = false,
                this.currentPage = 1,  
                this.pageNum = 1;
                this.results = res.body.result.reslist,
                this.ccfconferences = res.body.result.ccf_confs,
                this.conferences = res.body.result.confs,
                this.times = res.body.result.years,
                this.authors = res.body.result.authors,
                this.total = res.body.result.num,
                this.$router.push({
                    path: '/detail?q='+this.search+''
                })
            }) 
        },
        getConfList() {
               this.loading = true  
               this.$http.post('http://39.105.69.251:8081/search_post/', {
                query:this.search,
                year: this.timeValue,
                authors: this.authorValue,
                conf: this.selectConf,
                index: 1,
                sort: this.sort
            }).then(res => {  
                this.loading = false,
                this.currentPage = 1,  
                this.pageNum = 1, 
                this.results = res.body.result.reslist,
                this.times = res.body.result.years,
                this.authors = res.body.result.authors,
                this.total = res.body.result.num 
                
            }) 
        }
    },
    created () {
        this.getOriginList()
    }
}
</script>

<style> 
#detail {
    width: 100%;
    overflow: scroll;
    left: 0;
    position: absolute;
    top: 0;
    text-align: left;
    color: #000;
}
.top {
    border-bottom: 1px solid #ccc;
}
.top-content {
    height: 130px;
    margin: 0 auto;
    display: flex;
    width: 90%;
}
.logo {   
    margin: 0 20px 0 0;
    width:330px;
}
.logo a {
    font-size: 48px;
    line-height: 130px;
    font-weight: bolder;
    text-decoration: none;
    color: #000;
}
.search {
    /* flex: 1; */
    /* padding-top: 35px; */
    display: flex;
}
.sort-box {
    margin: 10px 0 0 0;
}
.sort-box .sortType,.selectedType:hover {
    cursor: pointer;
}
.results {
     color: rgb(173,35,51);
     font-size: 13px;
     padding-top: 4px;
}
.sortType {
    border: 1px solid #ccc;
    color: #ccc;
    border-radius: 5px;
    padding: 2px;
    margin: 0 2px;
}
.selectedType {
    border: 1px solid #ccc;
    background: #ccc;
    border-radius: 5px;
    padding: 2px;
    color: white;
    margin: 0 2px;
}
.input-with-select {
    background-color: #fff;
}
.el-input-group--append .el-input__inner, .el-input-group__prepend {
    height: 49px;
}
.el-input-group__prepend {
    background-color: #fff;
}
.el-input-group__append {
    background-color: #fff;
}








.bottom {
    padding: 0 0 20px 0;
    min-width: 700px;
}
.bottom-content {
    width: 90%;
    margin: 0 auto;
    display: flex; 
}
.select-opt {
    width: 330px;
    background-color: #fff;
    margin-right: 20px;
}
.conf-title {
    height: 70px;
    background-color: rgba(181,73,91,0.2);
    color: rgb(133,15,31);
    text-align: center;
}
.conf-subtitle {
    color: rgb(133,15,31);
    font-weight: bold;
    text-decoration: underline;
}
.conf-subtitle:hover {
    cursor: pointer;
}
.conf-title span {
    line-height: 70px; 
    font-size: 30px; 
}
.el-checkbox {
    width: 160px;
    margin: 0 !important;
    overflow-x: scroll;
    overflow-y: hidden;
    float: left;
    color: rgb(133,15,31)!important;
    padding:10px 0 10px 5px;
    cursor: pointer;
}
.el-checkbox__label {
    font-size: 20px!important;
    color: rgb(133,15,31)!important;
}
.result {
    background-color: #fff;
    /* width: 60%; */
    margin: 0 auto;
    padding: 5px 0 5px 0;
    flex:1;
}
.page {
    padding-top: 30px;
    margin: 0 auto;
    width: 400px;
}
.res-item {
    padding: 0 0 6px 0;
    border-bottom: 1px solid #ccc;
}
.title {
    /* font-size:1.1vw; */
    font-size:22px;
    padding-top:10px;
    font-weight:bold;
    padding: 10px 20px 0 1vw;
}
.detail-info {
    /* font-size: 0.9vw; */
    font-size: 18px;
    color: rgb(164,164,164);
    padding-top:2px;
    padding: 0 1vw;
}
.notOpen {
    /* font-size: 1.0vw; */
    font-size:16px;
    width:98%;
    margin-bottom: 4px;
    overflow:hidden; 
    text-overflow:ellipsis;
    display:-webkit-box;    
    -webkit-box-orient:vertical;
    -webkit-line-clamp:3;
    padding: 0 1vw;
}
.summary-all {
    /* font-size: 1.0vw; */
    font-size:16px;
    width:98%;
    margin-bottom: 4px;
    padding: 0 1vw;
}
.notOpen div {
    padding-right: 20px;
}
.summary-all div {
    padding-right: 20px;
}
.title-link {
    text-decoration: none;
    color: #2c3e50;
}
.author-link {
    color: rgb(164,164,164);
    padding-right: 8px;
    font-style:italic;
}
.summary-link {
    text-decoration: none;
    color: #2c3e50;
}
.footer {
    padding:30px 0 0 0;
    /* font-size: 0.9vw; */
    font-size: 14px;
}
.footer-content {
    width:400px;
    margin: 0 auto;
}
</style>