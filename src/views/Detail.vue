<template>
<div id="detail">
    <div class="top-content">
        <div class="logo">
            <a href="/">HCIHUB</a>
        </div>
        <div class="search">
            <el-input v-model="newSearch" class="input-with-select" @keyup.enter.native="getNewList()">
                <el-select v-model="timeValue" multiple placeholder="time" slot="prepend" style="width:80px;" collapse-tags>
                    <el-option
                        v-for="(time,index) in times"
                        :key="index"
                        :label="time"
                        :value="time">
                    </el-option>
                </el-select>
                <el-select v-model="authorValue" multiple placeholder="author" slot="append" style="width:150px;" collapse-tags>
                    <el-option
                    v-for="(author,index) in authors"
                    :key="index"
                    :label="author"
                    :value="author">
                    </el-option>
                </el-select>
                <el-button slot="append" icon="el-icon-search" style="margin-left:30px" @click="getNewList()"></el-button>
            </el-input>
            <span class="results">results:{{total}}</span>
        </div>
    </div>
    <div class="bottom">
        <div class="bottom-content">
            <div class="select-opt">
                <div class="conf-title">
                    <span>conferences</span>
                </div>
                <div>
                    <div class="conf-subtitle">CCF</div>
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
                        <a :href="result.url" class="title-link" target="_blank">{{(currentPage-1)*pageSize+index+1}}.</a>
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
                        layout="sizes, prev, pager, next"
                        :page-count="Math.floor(total/10)">
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
            search:'',
            input:'',
            newSearch:this.$route.query.q,
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
            // resNum:[],
            selectConf: [],
            total: 0,
            showOtherConf: false
        }
    },
    mounted() {
        
    },
    methods: {  
       more() {
            this.showOtherConf = ! this.showOtherConf
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
           this.$http.post('http://39.105.69.251:8081/search_post/', {
                query:this.newSearch,
                year: this.timeValue,
                authors: this.authorValue,
                conf: this.selectConf,
                index: val+1
            }).then(res => {
                this.results = res.body.result.reslist,
                // this.resNum = res.body.result.num,
                this.currentPage = val;
                this.$router.push({
                    path: '/detail?q='+this.newSearch+''
                })
            }).catch (err => {
                console.log(err)
            })
       },
       getOriginList() {
            this.$http.post('http://39.105.69.251:8081/search_post/', {
                query:this.search,
                year: [],
                authors: [],
                conf: [],
                index: 1
            }).then(res => {     
                console.log(res.body.result.num) 
                this.results = res.body.result.reslist,
                // this.resNum = res.body.result.num,
                this.ccfconferences = res.body.result.ccf_confs,
                this.conferences = res.body.result.confs,
                this.times = res.body.result.years,
                this.authors = res.body.result.authors ,
                this.total = res.body.result.num
            })
        },
        getNewList() {
            this.results = [],
            // this.resNum = [],
            this.ccfconferences = [],
            this.conferences = [],
            this.times = [],
            this.authors = [],
            this.total = 0,
            this.$http.post('http://39.105.69.251:8081/search_post/', {
                query:this.newSearch,
                year: this.timeValue,
                authors: this.authorValue,
                conf: this.selectConf,
                index: this.currentPage
            }).then(res => {
                this.results = res.body.result.reslist,
                // this.resNum = res.body.result.num,
                this.ccfconferences = res.body.result.ccf_confs,
                this.conferences = res.body.result.confs,
                this.times = res.body.result.years,
                this.authors = res.body.result.authors,
                this.total = res.body.result.num 
                //this.$router.push({
                //    path: '/detail?q='+this.newSearch+''
                //})
            }) 
        },
        getConfList() {
            setTimeout(() => {
               this.$http.post('http://39.105.69.251:8081/search_post/', {
                query:this.newSearch,
                year: this.timeValue,
                authors: this.authorValue,
                conf: this.selectConf,
                index: this.currentPage
            }).then(res => {  
                this.results = res.body.result.reslist,
                // this.resNum = res.body.result.num,
                this.ccfconferences = res.body.result.ccf_confs,
                this.conferences = res.body.result.confs,
                this.times = res.body.result.years,
                this.authors = res.body.result.authors,
                this.total = res.body.result.num 
                this.$router.push({
                    path: '/detail?q='+this.newSearch+''
                })
            }) 
            }, 5000);
        }
    },
    created () {
        this.search = this.$route.query.q,
        this.getOriginList()
    }
}
</script>

<style scoped> 
#detail {
    height: 100%;
    width: 100%;
    overflow: scroll;
    left: 0;
    position: absolute;
    top: 0;
    text-align: left;
}
.top-content {
    height: 100px;
    width: 73%;
    margin: 0 auto;
    display: flex;
    background-color: #fff;
}
.logo {   
    color: rgb(173,35,51);
    margin: 0 20px 0 0;
    width:240px;
}
.logo a {
    font-size: 55px;
    line-height: 100px;
    font-weight: bolder;
    text-decoration: none;
    color: rgb(173,35,51);
}
.search {
    flex: 1;
    padding-top: 30px;
}
.results {
     color: rgb(173,35,51);
     font-size: 13px;
}
.input-with-select {
    background-color: #fff;
}
.el-input-group__prepend {
    background-color: #fff;
}
.el-input-group__append {
    background-color: #fff;
}








.bottom {
    background-color: rgb(246,246,246);
    padding: 0 0 20px 0;
    min-width: 700px;
}
.bottom-content {
    width: 73%;
    margin: 0 auto;
    display: flex; 
}
.select-opt {
    width: 240px;
    background-color: #fff;
    margin-right: 20px;
}
.conf-title {
    height: 50px;
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
    line-height: 50px; 
    font-size: 20px; 
}
/* td {
    font-size: 12px;
    color: rgb(133,15,31);
    padding-right: 30px;
    cursor: pointer;
} */
.el-checkbox {
    width: 113px;
    margin: 0 !important;
    overflow-x: scroll;
    float: left;
    font-size: 13px;
    color: rgb(133,15,31);
    padding:10px 0 0 5px;
    cursor: pointer;
}
.result {
    background-color: #fff;
    width: 60%;
    margin: 0 auto;
    padding: 5px 0 5px 0;
    flex:1;
}
.page {
    padding-top: 30px;
}
.res-item {
    border-bottom: 1px solid #ccc;
}
.title {
    font-size:1.1vw;
    padding-top:10px;
    font-weight:bold;
    padding: 10px 20px 0 1vw;
}
.detail-info {
    font-size: 0.9vw;
    color: rgb(164,164,164);
    padding-top:1px;
    padding: 0 1vw;
}
.notOpen {
    font-size: 1.0vw;
    width:98%;
    margin-bottom: 3px;
    overflow:hidden; 
    text-overflow:ellipsis;
    display:-webkit-box;    
    -webkit-box-orient:vertical;
    -webkit-line-clamp:3;
    padding: 0 1vw;
}
.summary-all {
    font-size: 1.0vw;
    width:98%;
    margin-bottom: 3px;
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
    padding:10px;
    font-size: 0.9vw;
}
.footer-content {
    width:280px;
    margin: 0 auto;
}
</style>