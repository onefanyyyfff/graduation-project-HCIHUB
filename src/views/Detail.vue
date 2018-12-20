<template>
<div id="detail">
    <div class="top-content">
        <div class="logo">
            <a href="/">HCIBIB</a>
        </div>
        <div class="search">
            <el-input v-model="newSearch" class="input-with-select" @keyup.enter.native="getNewList()">
                <el-select v-model="timeValue" multiple placeholder="time" slot="prepend" style="width:150px;" collapse-tags>
                    <el-option
                        v-for="(time,index) in times"
                        :key="index"
                        :label="time"
                        :value="time">
                    </el-option>
                </el-select>
                <el-select v-model="authorValue" multiple placeholder="author" slot="append" style="width:200px;" collapse-tags>
                    <el-option
                    v-for="(author,index) in authors"
                    :key="index"
                    :label="author.name"
                    :value="author.name">
                    </el-option>
                </el-select>
                <el-button slot="append" icon="el-icon-search" style="margin-left:30px" @click="getNewList()"></el-button>
            </el-input>
        </div>
    </div>
    <div class="bottom">
        <div class="bottom-content">
            <div class="select-opt">
                <div class="conf-title">
                    <span>conferences</span>
                </div>
                <table class="conf-select">
                    <tbody>
                        <tr v-for="(n,index) in Math.round(conferences.length/2)" :key="index">
                            <td @click="getNewList(2*n-2)">{{conferences[2*n-2]}}</td>
                            <td @click="getNewList(2*n-1)">{{conferences[2*n-1]}}</td>
                        </tr>
                    </tbody>
                </table>               
            </div>
            <div class="result">
                <div v-for="(result,index) in results.slice((currentPage-1)*pageSize,currentPage*pageSize)" :key="index" class="res-item">
                    <div class="title">
                        <a :href="result.url" class="title-link" target="_blank">{{(currentPage-1)*pageSize+index+1}}.</a>
                        <a :href="result.url" class="title-link" target="_blank"><span v-html="result.title"></span></a>
                    </div>
                    <div class="detail-info">
                        <span>{{result.date}} </span>
                        <span>{{result.conf}} </span>
                        <a v-for="(author,index) in result.authors" :key="index" :href="author.link" class="author-link" target="_blank">{{author.name}}</a>
                    </div>
                    <div class="summary" v-if="!result.openFlag" @click="showPieceFunc(result,index)">
                        <div>Summary:<span v-html="result.summary"></span></div>
                    </div>
                    <div class="summary-all" v-else @click="showPieceFunc(result,index)">
                        <div>Summary:<span v-html="result.summary"></span></div>
                    </div>
                </div>
            </div>
        </div>  
        <div class="page">
            <el-pagination
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page.sync="currentPage"
                :page-sizes="[10, 20, 50, 100,200]"
                :page-size="pageSize"
                layout="sizes, prev, pager, next"
                :page-count="Math.ceil(results.length/pageSize)">
            </el-pagination>
        </div>
    </div>
    <div class="footer">
        <div class="footer-content">Copyright © 2017 清华大学 · 人机交互实验室 </div>
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
            timeValue:'',
            authorValue:'',
            conferenceValue:'',
            times: [],
            authors:[],
            conferences:[],
            results: [],
            currentPage: 1,
            pageSize:10,
            screenWidth:'',
            showPiece: []
        }
    },
    mounted() {
        
    },
    watch: {
        screenWidth (val) {
            this.screenWidth = val
        }
    },
    methods: {   
       changeTopContent() { 
            if(this.screenWidth >500) {
                console.log(this.screenWidth)
            }
       }, 
       showPieceFunc(result,index) {
        //    if(this.showPiece.indexOf(index) == -1) {
        //        this.showPiece.push(index)
        //    }
        //    else {
        //        this.showPiece.splice(this.showPiece.indexOf(index),1)
        //    }
            if(!result.openFlag) {
                Vue.set(result,'openFlag',true)
            }
            else {
                Vue.set(result,'openFlag',false)
            }
       },
       handleSizeChange(val) {
           this.pageSize = val
            console.log(`每页 ${val} 条`);
       },
       handleCurrentChange(val) {
           this.currentPage = val;
            console.log(`当前页: ${val}`);
       },
       getOriginList() {
            this.$http.get(`http://166.111.139.127:8080/search/?query=${this.search}`)
            .then(res => {
                console.log(res)
                //all result
                this.results = res.body;
                this.results.sort(this.sortResult('date'))
                //time
                for(let i = 0;i<this.results.length;i++) {
                    this.times.push(this.results[i].date)
                }
                this.times = Array.from(new Set(this.times))
                this.times.sort(this.sortTime)
                //authors
                for(let i = 0;i<this.results.length;i++) {
                    for(let j=0;j<this.results[i].authors.length;j++) {
                        this.authors.push(this.results[i].authors[j])
                    }
                }
                this.authors = Array.from(new Set(this.authors))
                this.authors.sort()
                //conf
                for(let i = 0;i<this.results.length;i++) {
                    this.conferences.push(this.results[i].conf)
                }
                this.conferences = Array.from(new Set(this.conferences))
                this.conferences.sort()
                console.log(this.conferences)
            })
        },
        sortResult(property){
            return function(a,b) {
                var value1 = a[property];
                var value2 = b[property];
                return value2-value1
            }
        },
        sortTime(a,b)
        {
            return b - a
        },
        getNewList(n) {
            this.$http.post('http://166.111.139.127:8080/search_post/', {
                query:this.newSearch,
                year: this.timeValue,
                authors: this.authorValue,
                conf: n ? [this.conferences[n]] : []
            }).then(res => {
                this.results = res.body;
                this.results.sort(this.sortResult('date'))
                for(let i = 0;i<this.results.length;i++) {
                    this.times.push(this.results[i].date)
                }
                this.times = Array.from(new Set(this.times))
                this.times.sort(this.sortNumber)
                for(let i = 0;i<this.results.length;i++) {
                    for(let j=0;j<this.results[i].authors.length;j++) {
                        this.authors.push(this.results[i].authors[j])
                    }
                }
                this.authors = Array.from(new Set(this.authors))
                this.authors.sort()
                for(let i = 0;i<this.results.length;i++) {
                    this.conferences.push(this.results[i].conf)
                }
                this.conferences = Array.from(new Set(this.conferences))
                this.conferences.sort()
                this.$router.push({
                    path: '/detail?q='+this.newSearch+''
                })
            })
        }
    },
    created () {
        this.search = this.$route.query.q,
        this.getOriginList(),
        this.changeTopContent()
    }
}
</script>

<style scoped> 
#detail {
    height: 100%;
    width: 100%;
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
    width:200px;
}
.logo a {
    font-size: 50px;
    line-height: 100px;
    font-weight: bolder;
    text-decoration: none;
    color: rgb(173,35,51);
}
.search {
    flex: 1;
    padding-top: 30px;
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
    width: 200px;
    background-color: #fff;
    margin-right: 20px;
}
.conf-title {
    height: 50px;
    background-color: rgba(181,73,91,0.2);
    color: rgb(133,15,31);
    text-align: center;
}
.conf-title span {
    line-height: 50px; 
    font-size: 20px; 
}
td {
    font-size: 12px;
    color: rgb(133,15,31);
    padding-right: 30px;
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
    width:500px;
    margin: 0 auto;
    padding-top: 30px;
}
.res-item {
    border-bottom: 1px solid #ccc;
}
.title {
    font-size:1.1vw;
    padding-top:10px;
    font-weight:bold;
    padding: 10px 20px 0 20px;
}
.detail-info {
    font-size: 0.9vw;
    color: rgb(164,164,164);
    padding-top:1px;
    padding: 0 20px;
}
.summary {
    font-size: 1.0vw;
    width:98%;
    margin-bottom: 3px;
    overflow:hidden; 
    text-overflow:ellipsis;
    display:-webkit-box;    
    -webkit-box-orient:vertical;
    -webkit-line-clamp:3;
    padding: 0 20px;
}
.summary-all {
    font-size: 1.0vw;
    width:98%;
    margin-bottom: 3px;
    padding: 0 20px;
}
.summary div {
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