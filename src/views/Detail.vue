<template>
<div id="detail">
    <div class="top-content">
        <!-- <div class="search">
            HCIHUB
            <el-input v-model="newSearch" class="input-with-select">
                <el-select v-model="timeValue" multiple placeholder="time" slot="prepend" style="width:120px;">
                    <el-option
                        v-for="(time,index) in times"
                        :key="index"
                        :label="time"
                        :value="time">
                    </el-option>
                </el-select>
                <el-select v-model="authorValue" multiple placeholder="author" slot="append" style="width:200px;">
                    <el-option
                    v-for="(author,index) in authors"
                    :key="index"
                    :label="author.name"
                    :value="author.name">
                    </el-option>
                </el-select>
                <el-select v-model="conferenceValue" multiple placeholder="conference" slot="append" style="width:150px;margin-left:30px;">
                    <el-option
                    v-for="(conference,index) in conferences"
                    :key="index"
                    :label="conference"
                    :value="conference">
                    </el-option>
                </el-select>
                <el-button slot="append" icon="el-icon-search" style="margin-left:30px" @click="getNewList()"></el-button>
            </el-input>
        </div> -->
        <div class="logo">
            HCIBIB
        </div>
        <div class="search">
            <el-input v-model="newSearch" class="input-with-select">
                <el-select v-model="timeValue" multiple placeholder="time" slot="prepend" style="width:150px;" collapse-tags>
                    <el-option
                        v-for="(time,index) in times"
                        :key="index"
                        :label="time"
                        :value="time">
                    </el-option>
                </el-select>
                <el-select v-model="authorValue" multiple placeholder="author" slot="append" style="width:250px;" collapse-tags>
                    <el-option
                    v-for="(author,index) in authors"
                    :key="index"
                    :label="author.name"
                    :value="author.name">
                    </el-option>
                </el-select>
                <el-select v-model="conferenceValue" multiple placeholder="conference" slot="append" style="width:150px;margin-left:30px;" collapse-tags>
                    <el-option
                    v-for="(conference,index) in conferences"
                    :key="index"
                    :label="conference"
                    :value="conference">
                    </el-option>
                </el-select>
                <el-button slot="append" icon="el-icon-search" style="margin-left:30px" @click="getNewList()"></el-button>
            </el-input>
        </div>
    </div>
    <div class="bottom-content">
        <div class="result">
            <!-- <div class="sort-way">
                <span></span>
            </div> -->
            <div v-for="(result,index) in results.slice((currentPage-1)*pageSize+1,currentPage*pageSize+1)" :key="index" class="res-item">
                <div class="title">
                    <a :href="result.url" class="title-link" target="_blank">{{index+1}}.</a>
                    <a :href="result.url" class="title-link" target="_blank"><span v-html="result.title"></span></a>
                </div>
                <div class="detail-info">
                    <span>{{result.date}} </span>
                    <span>{{result.conf}} </span>
                    <a v-for="(author,index) in result.authors" :key="index" :href="author.link" class="author-link" target="_blank">{{author.name}}</a>
                </div>
                <div class="summary">
                    <a  :href="result.url" class="summary-link" target="_blank"><p>Summary:<span v-html="result.summary"></span></p></a>
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
                :total="1000">
            </el-pagination>
        </div>
    </div>  
    <div class="footer">
        <div class="footer-content">Copyright © 2017 清华大学 · 人机交互实验室 </div>
    </div> 
</div>
</template>
<script>
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
            pageSize:10
        }
    },
    mounted() {
        
    },
    methods: {    
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
        getNewList() {
            this.$http.post('http://166.111.139.127:8080/search_post/', {
                query:this.newSearch,
                year: this.timeValue,
                authors: this.authorValue,
                conf: this.conferenceValue
            }).then(res => {
                console.log(res)
                this.results = res.body;
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
        this.getOriginList()
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
.search {
    width: 70%;
    margin: 0 auto;
    padding-top: 2.3%;
}
.top-content {
    height: 15%;
}
.logo {
    font-size: 3.7vw;
    font-weight: bolder;
    color: rgb(173,35,51);
    margin: 1% 0 0 1.8vw;
    float: left;
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








.bottom-content {
    background-color: rgb(246,246,246);
    padding: 0 0 20px 0;
    min-width: 700px;
}
.result {
    background-color: #fff;
    width: 70%;
    margin: 0 auto;
    padding: 5px 0 5px 0;
    /* box-shadow:  rgb(230,227,228) 0px 0px 20px; */
}
.page {
    width:500px;
    margin: 0 auto;
    padding-top: 30px;
}
.sort-way {
    height: 50px;
    background-color: rgba(181,73,91,0.2);
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
    position: relative;
    top: -9px;
    height: 93px;
    width:98%;
    margin-bottom: 4px;
    overflow:hidden; 
    text-overflow:ellipsis;
    display:-webkit-box;    
    -webkit-box-orient:vertical;
    -webkit-line-clamp:4;
    padding: 0 20px;
}
.summary p {
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