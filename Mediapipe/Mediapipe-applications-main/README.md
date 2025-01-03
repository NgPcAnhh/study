📋 Giới thiệu
Đây là bộ sưu tập các ứng dụng tương tác sáng tạo sử dụng thư viện MediaPipe của Google. MediaPipe cung cấp các giải pháp machine learning thời gian thực mạnh mẽ và dễ dàng tích hợp. Với Python, chúng tôi đã xây dựng 3 project thú vị tập trung vào việc nhận diện cử chỉ tay và tương tác với máy tính thông qua hình ảnh/video từ camera. Các ứng dụng cụ thể bao gồm:

1. Phát hiện cử chỉ tay (Hand Gesture Detection)
Mô tả: Ứng dụng này sử dụng MediaPipe Hands để phát hiện bàn tay và nhận diện các cử chỉ như "like", "peace", "stop", hoặc cử chỉ tùy chỉnh khác. Hệ thống có thể được áp dụng để điều khiển các thiết bị hoặc giao tiếp mà không cần sử dụng lời nói.
Tính năng:
Phát hiện bàn tay và ngón tay từ camera thời gian thực.
Nhận diện các cử chỉ tay dựa trên tọa độ keypoints.
Dễ dàng mở rộng để nhận diện cử chỉ tùy chỉnh theo nhu cầu.
Ứng dụng thực tế:
Điều khiển trình chiếu hoặc phần mềm.
Trợ lý ảo với điều khiển không chạm.
Ngôn ngữ sử dụng: Python

2. Flappy Bird điều khiển bằng ngón tay (Flappy Bird with Finger Control)
Mô tả: Đây là phiên bản sáng tạo của game Flappy Bird, nơi người chơi điều khiển chú chim bằng chuyển động của ngón tay. Bằng cách nâng và hạ ngón tay (hoặc bàn tay), người chơi có thể làm chú chim bay lên hoặc hạ xuống.
Tính năng:
Tích hợp MediaPipe Hands để theo dõi vị trí của ngón tay.
Thay đổi độ cao của chú chim theo chuyển động ngón tay.
Game logic được lập trình để mô phỏng trải nghiệm giống Flappy Bird gốc.
Ứng dụng thực tế:
Giải trí và khám phá cách điều khiển mới lạ.
Gợi ý ứng dụng cho điều khiển trò chơi bằng cử chỉ.
Ngôn ngữ sử dụng: Python

3. Trò chơi Đấm Lá Kéo với máy (Rock Paper Scissors AI)
Mô tả: Trò chơi kinh điển "Đấm Lá Kéo" được hiện thực hóa bằng cách sử dụng MediaPipe Hands để nhận diện cử chỉ tay của người chơi. Máy tính sẽ tự động chọn một lựa chọn và hiển thị kết quả dựa trên luật chơi.
Tính năng:
Nhận diện cử chỉ "Đấm", "Lá", "Kéo" thông qua keypoints của bàn tay.
Máy tính chọn lựa ngẫu nhiên kết quả (hoặc có thể tích hợp AI để dự đoán).
Hiển thị kết quả trên màn hình theo thời gian thực.
Ứng dụng thực tế:
Demo tương tác thị giác cho các ứng dụng giáo dục hoặc giải trí.
Nền tảng cho việc phát triển thêm các trò chơi nhận diện cử chỉ khác.
Ngôn ngữ sử dụng: Python
