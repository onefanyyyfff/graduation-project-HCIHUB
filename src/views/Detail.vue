<template>
<div id="detail">
    <div class="top-content">
        <div class="search">
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
        </div>
    </div>
    <div class="bottom-content">
        <div class="result">
            <div v-for="(result,index) in results" :key="index" class="res-item">
                <div class="title">
                    <a :href="result.url" class="title-link" target="_blank">{{index+1}}.</a>
                    <a :href="result.url" class="title-link" target="_blank"><span v-html="result.title"></span></a>
                </div>
                <div class="detail-info">
                    <span>{{result.conf}}  ·  </span>
                    <a v-for="(author,index) in result.authors" :key="index" :href="author.link" class="author-link" target="_blank">{{author.name}}</a>
                    <span>{{result.date}}  </span>
                </div>
                <div class="summary">
                    <a  :href="result.url" class="summary-link" target="_blank"><p>Summary:<span v-html="result.summary"></span></p></a>
                </div>
            </div>
        </div>
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
            results: []
        }
    },
    mounted() {
        
    },
    methods: {    
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
    width: 75%;
    margin: 0 auto;
    padding-top: 3%;
}
.top-content {
    height: 18%;
}
.el-select .el-input {
    width: 130px;
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
    padding: 20px 0;
    min-width: 700px;
}
.result {
    background-color: #fff;
    width: 75%;
    margin: 0 auto;
    padding: 20px;
    box-shadow:  rgb(230,227,228) 0px 0px 20px;
}
.res-item {
    border-bottom: 1px solid #ccc;
}
.title {
    font-size:1.1vw;
    padding-top:10px;
}
.detail-info {
    font-size: 0.9vw;
    color: rgb(164,164,164);
}
.summary {
    font-size: 0.9vw;
}
.title-link {
    text-decoration: none;
    color: #2c3e50;
}
.author-link {
    text-decoration: none;
    color: rgb(164,164,164);
    padding-right: 10px;
}
.summary-link {
    text-decoration: none;
    color: #2c3e50;
}
</style>