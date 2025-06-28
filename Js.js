var loadHucCong = false;
if (window.sessionStorage){
    var data = sessionStorage.getItem('time_load_gpmn');
    if (data) loadHucCong = false;
    else loadHucCong = true;
}
document.addEventListener("DOMContentLoaded", function() {
  if (!loadHucCong) return;
  var body = document.body;
  var elemDiv = document.createElement('div');
  elemDiv.setAttribute('id','gpmn-body-load')
  elemDiv.innerHTML=`<div class="bl-logo">
          <div class="tank-wrap">
              <div class="vn-sun"><img src="https://api.cmsnt.co/cdn/3041975/img/vn-flag-full.gif" /></div>
              <div class="tank-simu">
                  <div class="wheels"><span></span><span></span><span></span><span></span><span></span></div>
                  <div class="fence"></div>
                  <div class="fence2"></div>
              </div>
              <div class="gate"></div>
              <div class="gate2"></div>
          </div>
          <div class="text-h1 text-center">Chào mừng 50 năm thống nhất đất nước Việt Nam</div>
      </div>`;
  document.body.appendChild(elemDiv);
  setTimeout(function() {
          document.getElementById('gpmn-body-load').style.display = 'none';
      }, 3100);
  if (window.sessionStorage){
   sessionStorage.setItem('time_load_gpmn', 1);

  }
});
function createSakura() {
    const sakura = document.createElement("div");
    sakura.classList.add("sakura");

    // Đặt vị trí ngẫu nhiên cho cánh hoa
    sakura.style.left = Math.random() * 100 + "vw";  // Tạo vị trí ngẫu nhiên từ trái sang phải

    // Điều chỉnh thời gian rơi ngẫu nhiên (5s đến 12s) cho hoa
    const duration = Math.random() * 20 + 10;  // Tạo thời gian rơi từ 5s đến 15s
    sakura.style.animationDuration = `${duration}s`;

    // Tăng kích thước hoa ngẫu nhiên
    let size = Math.random() * 300 + 200;  // Kích thước hoa từ 50px đến 100px
    sakura.style.width = size + "px";
    sakura.style.height = size + "px";

    // Thêm cánh hoa vào container
    document.getElementById("sakura-container").appendChild(sakura);

    // Xóa cánh hoa sau khi rơi xong
    setTimeout(() => {
        sakura.remove();
    }, duration * 1000);  // Dùng thời gian rơi để xóa hoa sau khi rơi xong
}

// Giảm số lượng hoa rơi lại (giảm tốc độ tạo hoa)
setInterval(createSakura, 6000);  // Mỗi 2 giây tạo ra một cánh hoa mới (chậm lại so với 1 giây)

