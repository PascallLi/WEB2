    var api = {}
    // callback为回调函数，将response数据处理完成之后的数据传回bindEventWeiboAdd中的reponse = function(r)
    api.ajax = function(url, method, form, callback) {
        var data = JSON.stringify(form)
        // 将类转成字符串格式
          console.log('data==', data)
        // object转换成字符串
        var request = {
            url: url,
            type: method,
            // data: form,
            // 目的是将发送的数据以字符串形式传，而不是类
            contentType: 'application/json; charset=utf-8',
            // 发送的是json格式
            // dataType: 'json',
            // 指定返回的数据类型
            data:　data,

            // 这里的success指的是得到的响应回复200-300，返回的字符串数据由后端json.dumps提供
            success: function(response) {
              console.log(response)
              // var r = response
              // 从服务器得到的响应为json格式
              var r = JSON.parse(response)
              console.log('r===', r)
              // r=== Object { data: Object, message: "", success: true }
              callback(r)
              // response = {"data": {"comments_num": 0, "id": 7, "weibo": "再来吧",
              // "avatar": "http://vip.cocode.cc/uploads/avatar/192.gif", "name": "123",
              // "created_time": "2016/11/25 16:32:37"}, "success": true}
              // r 就是后台发送的字符串response转换成类
            },
            error: function(error){
              console.log('网络错误', error)
              var r = {
                'success': false,
                message: '网络错误',
              }
              callback(r)
            }
        }
        $.ajax(request)
        // 发给浏览器
    }
    api.post = function(url, form, callback){
       api.ajax(url, 'post', form, callback)
    }
    api.weiboAdd = function(form, callback){
      var url = '/weibo/add'
      api.post(url, form, callback)
    }
    api.weiboDelete = function(weiboId, callback){
      var url = '/delete/' + weiboId
      var form = {}
      // 没有form,就传空的过去
      api.post(url, form, callback)
    }
    api.update = function(form, callback) {
      var url = '/weibo/update'
      api.post(url, form, callback)
    }
    api.Comment =  function(form, callback){
     var url = '/comment/add'
     api.post(url, form, callback)
    }
    var weiboTemplate = function(content){
        var w = content
        var t = `
              <div class='edit-comment'>
              ${w.created_time }
                &nbsp;
                <a href="" class="post-title-link">&nbsp;编辑</a>
                &nbsp;
                <button class="weibo-delete" data-id= ${ w.id }>删除</button>
                  <div class='comment-api'>
                      <form action="/comment/add" method="post">
                        <input type="hidden" name="weibo_id" value= ${ w.id}>
                        <input  type="text" name="comment" class="power-comment-content">
                        <button type="submit" class="power-comment-button">评论</button>
                      </form>
                  </div>
                  <div class="article-body">
                      <p> ${w.content} </p>
                  </div>

            </div>
        `
        return t
      }

      var weiboComment = function(content){
          var c = content
          var t  = `
          <div class="comments">
            <br>
            ${ c.comment }
            <br>
            ${ c.created_time }
            <br>
          </div>

          `
          return t
      }
      var bindEvents = function() {
            // 不同的事件用不同的函数去绑定处理
            // 这样逻辑就非常清晰了
            bindEventCommentToggle()
            bindEventWeiboAdd()
            bindEventWeiboComment()
            bindEventWeiboDelete()

        }

        // 页面载入完成后会调用这个函数，所以可以当做入口
        $(document).ready(function(){
            // 用 bindEvents 函数给不同的功能绑定事件处理
            // 这样逻辑就非常清晰了
            bindEvents()
        })
        // 编辑按钮触发功能
       var bindEventCommentToggle = function() {
          $('a.post-title-link').on('click', function(){
              // 对编辑选项进行点击
              console.log('触发3')
              $(this).next().next().slideToggle()
              // 输入框点击隐藏，a属性会跳转，默认阻止
              return false;
        })
      }
        // 添加微博功能
        var bindEventWeiboAdd = function() {
              $('#id-button-weibo-add').on('click', function(){
                    console.log('触发')
                    var content = $('#id-input-weibo').val()
                    var form = {
                      content : content,
                    }
                    console.log('content==', form.content)
                    // response 是回调函数，r是一个类，ajax请求结束以后返回到这里执行后面的语句
                    var response = function(r){
                      console.log('成功', r)
                      if (r.success) {
                        var w = r.data
                        $('.box').prepend(weiboTemplate(w))
                        alert("添加成功")
                      }
                      else {
                        alert(r.message)
                      }
                    }
              api.weiboAdd(form, response)
              })
        }
        //  添加评论功能
        var bindEventWeiboComment = function() {
           $('.power-comment-button').on('click', function(){
               console.log('评论触发成功')
               var content = $(this).parent().find('.power-comment-content').val()
               // var id = $(this).closest('.comment-api').find('.weibo_id').val()
               var id = $(this).closest('.box').find('.weibo-delete').data('id')
               console.log('content', content)
               var form = {
                content: content,
                weibo_id: id,
               }
               var response = function(r){
                console.log('评论反馈成功')
                if (r.success) {
                 var c = r.data
                 $(this).closest('.comments').append(weiboComment(c))
                 alert('评论成功')
                }
                else {
                 alert(r.message)
                }
               }
            api.Comment(form, response)
           })


        }

        // 删除功能，需要把事件绑定在父元素，父元素不会被删除（事件委托）
          var bindEventWeiboDelete = function(){
              $('.box').on('click', '.weibo-delete', function(){
                  console.log('触发2')
                  var weiboId =  $(this).data('id')
                  console.log('weiboId=', weiboId)
                  var weiboCell = $(this).closest('.edit-comment')
                  console.log('weibocell=', weiboCell)
                  //  closest是离这个元素往上找最近的某个元素
                  // success 和 error 统称回掉函数
                  api.weiboDelete(weiboId, function(response) {
                      var r = response
                      if (r.success) {
                        $(weiboCell).slideUp()
                        console.log('成功', arguments)
                        alert("删除成功")
                      }
                      else {
                        console.log('失败', arguments)
                        alert("删除失败")
                      }
                  })

                })
              }
