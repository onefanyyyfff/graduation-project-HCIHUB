<template>
<div id="detail" v-loading="loading">
    <div class="top">
        <div class="top-content">
            <div class="logo" ref="logo">
                <a href="/"><span style="color:#4AA5E5">HCI</span><span style="color:#FCB75F">HUB</span></a>
            </div>
            <div class="search">
                <el-select v-model="timeValue" multiple placeholder="time" slot="prepend" style="width:120px;border:none" collapse-tags>
                    <el-option
                        v-for="(time,index) in times"
                        :key="index"
                        :label="time"
                        :value="time">
                    </el-option>
                </el-select>
                <input v-model="search" class="input-with-select" @keyup.enter="getNewList()">
                <img src="../../static/search.png" @click="getNewList()">
            </div>
        </div>
    </div>
    <div class="sort-box">
        <div class="results">results:{{total}}</div>
        <div :class="{selectedType:sort===1,sortType:sort!==1}" @click="getNewSort(1)">RELAVANCE</div>
        <div :class="{selectedType:sort===2,sortType:sort!==2}" @click="getNewSort(2)">TIME</div>
    </div>
    <div class="bottom">
        <div class="bottom-content">
            <div class="select-opt">
                <div class="conf-title">
                    <span>Source</span>
                </div>
                <div>
                    <el-checkbox-group v-model="selectConf" @change="getConfList" style="height:250px">
                        <el-checkbox v-for="(item,index) in ccfconferences" :key="index" :index="index" :label="item._id+':'+item.cnt" >
                            <div class="check-label">
                                <div>{{item._id}}</div>
                                <div class="check-num">{{item.cnt}}</div>
                            </div>                 
                        </el-checkbox>
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
                        <div>Summary:<div v-html="result.summary"></div></div>
                    </div>
                    <div class="summary-all" v-else @click="showPieceFunc(result,index)">
                        <div>Summary:<div v-html="result.summary"></div></div>
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
    height: 124px;
    margin: 0 auto;
    display: flex;
    width: 90%;
}
.logo {   
    margin: 0 40px 0 0;
    width:330px;
}
.logo a {
    font-size: 58px;
    line-height: 124px;
    font-weight: bolder;
    text-decoration: none;
    color: #000;
}
.search {
    /* flex: 1; */
    margin-top: 33px;
    display: flex;
    height: 50px;
    width: 690px;
    padding:4px;
    border: 1px solid #D8D8D8;
    border-radius: 13px;
}
.search input {
    width: 520px;
    height: 49px;
    outline: none;
    border: none;
    font-size: 25px;
    z-index: 999;
}
.search img {
    width: 36px;
    height: 36px;
    padding: 7px 0;
}
.sort-box {
    width: 90%;
    margin: 0 auto;
    padding: 24px 0;
    display: flex;
}
.sort-box .sortType,.selectedType:hover {
    cursor: pointer;
}
.results {
     color: #000;
     font-size: 15px;
     padding-top: 4px;
     width: 330px;
     margin: 0 40px 0 0 
}
.sortType {
    border: 1px solid #BABABA;
    color: #BABABA;
    border-radius: 5px;
    padding: 0 12px;
    margin: 0 24px 0 0;
    height:31px;
    line-height: 31px;
}
.selectedType {
    border: 1px solid #4AA5E5;
    border-radius: 5px;
    padding: 0 12px;
    color: #4AA5E5;
    margin: 0 24px 0 0;
    height: 31px;
    line-height: 31px;
}
.input-with-select {
    background-color: #fff;
}
.el-input-group__append {
    background-color: #fff;
}








.bottom {
    padding: 0 0 20px 0;
    /* min-width: 700px; */
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
    color: #000;
    text-align: left;
    border-top: 1px solid #BABABA;   
}
.conf-subtitle {
    font-weight: bold;
    text-decoration: underline;
}
.conf-subtitle:hover {
    cursor: pointer;
}
.conf-title span {
    line-height: 70px; 
    font-size: 28px; 
    font-weight: bold;
}
.el-checkbox {
    width: 330px;
    margin: 0 !important;
    /* overflow-x: scroll;
    overflow-y: hidden; */
    float: left;
    /* color: rgb(133,15,31)!important; */
    padding:10px 0 10px 5px;
    cursor: pointer;
}
.el-checkbox__label {
    font-size: 20px!important;
    /* color: rgb(133,15,31)!important; */
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
    padding: 0 0 50px 0;
}
.title {
    /* font-size:1.1vw; */
    font-size:22px;
    padding-top:10px;
    font-weight:bold;
    padding: 10px 20px 8px 1vw;
}
.detail-info {
    /* font-size: 0.9vw; */
    font-size: 14px;
    color: #A5A5A5;
    padding-top:2px;
    padding: 0 1vw;
}
.notOpen {
    /* font-size: 1.0vw; */
    font-size:19px;
    width:98%;
    margin-bottom: 4px;
    overflow:hidden; 
    text-overflow:ellipsis;
    display:-webkit-box;    
    -webkit-box-orient:vertical;
    -webkit-line-clamp:3;
    padding: 8px 1vw 0 1vw;
    text-align:justify
}
.summary-all {
    /* font-size: 1.0vw; */
    font-size:19px;
    width:98%;
    margin-bottom: 4px;
    padding: 0 1vw;
    text-align:justify;
    padding: 8px 1vw 0 1vw;
}
.notOpen div {
    padding-right: 20px;
}
.summary-all div {
    padding-right: 20px;
}
.title-link {
    text-decoration: none;
    color: #000;
}
.author-link {
    color: #A5A5A5;
    padding-right: 8px;
    text-decoration: none;
}
.summary-link {
    text-decoration: none;
    color: #000;
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



.el-checkbox__inner {
    border-radius: 0;
    border: none!important;
    /* background-color:#A8A8A8; */
  }
.el-checkbox {
    color: #000;
  }
.el-checkbox:hover {
    background: #F4F4F4;
    border-radius: 5px;
}
.el-checkbox__input.is-checked + .el-checkbox__label {
    color: #000!important;
    font-weight: bold;
  }
.el-checkbox__input.is-checked .el-checkbox__inner {
    background-color: #FCB75F!important;
    border-color: #FCB75F!important;
    border-radius: 7.5px!important;
    width: 15px!important;
    height: 15px!important;
  }
 .el-checkbox__input.is-checked .el-checkbox__inner::after {
  border: 2px solid #FCB75F;
  -webkit-box-sizing: content-box;
  box-sizing: content-box;
  content: "";
  border-left: 0;
  border-top: 0;
  height: 7px;
  left: 4px;
  position: absolute;
  top: 1px;
  width: 3px;
  -webkit-transform: rotate(45deg) scaleY(1);
  transform: rotate(45deg) scaleY(1);
}
.check-label {
    display: flex;
    justify-content: space-between;
    width: 250px;
}
.check-num {
    color: #A7A7A7;
}
.el-checkbox__input.is-checked + .el-checkbox__label .check-num {
    color: #000;
}
.el-checkbox__label {
    display: inline-block
}
</style>