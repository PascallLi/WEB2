
    var api = {}

    api.ajax = function(url, method, form, success, error) {
        var request = {
            url: url,
            type: method,
            data: form,
            success: success,
            error: error
        }
        $.ajax(request)
    }
    api.post = function(url, form, success, error){
       api.ajax(url, 'post', form, success, error)
    }
    api.weiboAdd = function(form, success, error){
      var url = '/weibo/add'
      api.post(url, form, success, error)
    }
    api.weiboDelete = function(weiboId, success, error){
      var url = '/delete/' + weiboId
      var form = {}
      // 没有form,就传空的过去
      api.post(url, form, success, error)
    }

      var weiboTemplate = function(content){
          var w = content
          var t = `
          <div class="box power-header">
              <h2 class="id-subtitle-line"></h2>

                <div class='edit-comment'>
                  ${ w.created_time }&nbsp;<a href="#" class="post-title-link">&nbsp;编辑</a>
                  &nbsp;
                  <button class="weibo-delete" data-id= ${ w.id }>删除</button>
                  </div>
                  <div class='comment-api'>
                  <form action="/comment/add" method="post">
                  <input type="hidden" name="weibo_id" value="${ w.id }">
                  <input  type="text" name="comment" class="power-comment-content">
                  <button type="submit" class="power-comment-button">评论</button>
                  </form>
                  </div>
              <div class="article-body">
                  <p>${w.content} </p>
              </div>
          </div>
          `
          return t
        }

  // 添加微博功能
    $(document).ready(function(){
        $('#id-button-weibo-add').on('click', function(){
            console.log('触发')
            var content = $('#id-input-weibo').val()
            var form = {
              content:content,
            }
            var success = function(response){
              // console.log('成功', arguments)
              console.log('response', response)
               var w = JSON.parse(response)
               $('.box').prepend(weiboTemplate(w))
             }
             var error = function(){
               console.log('错误', arguments)
             }
             api.weiboAdd(form, success, error)
          })


  // 删除功能，需要把事件绑定在父元素，父元素不会被删除（事件委托）

        $('.box').on('click', '.weibo-delete', function(){
            console.log('触发2')
            var weiboId =  $(this).data('id')
            console.log(weiboId)
            var weiboCell = $(this).closest('.edit-comment')
            //  closest是离这个元素往上找最近的某个元素
            // success 和 error 统称回掉函数
            var success = function(response) {
              console.log('成功', arguments)
              // 用动画删除
              // $(weiboCell).remove()
              $(weiboCell).slideUp()
            }
            var error = function() {
              console.log('错误', arguments)
            }
            api.weiboDelete(weiboId, success, error)

          })

      // 展开评论事件

          $('a.post-title-link').on('click', function(){
              // $(this).parent().next().slideToggle()
              $(this).next().next().slideToggle()
              // class='comment-api
              return false;
          })
      })
