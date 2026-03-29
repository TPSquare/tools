import ScriptManager from "./ScriptManager.js";
const manager = new ScriptManager(["audio"], ["sample"]);

manager.scenes([
  { sampleVideo: [manager.sampleVideos.sample, "0:00 - 0:12"], actors: ["Chí Vỹ", "Huỳnh Nhật", "Thành Vũ"], preparation: "2 quyển vở", location: "1" },
  { sampleVideo: [manager.sampleVideos.sample, "0:13 - 0:22"], actors: ["Tất cả"], location: "1" },
  { sampleVideo: [manager.sampleVideos.sample, "0:36 - 0:37.4"], actors: ["Công Đạt"], preparation: "Một cái cặp", location: "1" },
  { sampleVideo: [manager.sampleVideos.sample, "0:37.8 - 0:38.25"], actors: ["Duy Khang"], location: "1" },
  { sampleVideo: [manager.sampleVideos.sample, "0:38.5 - 0:39.5"], actors: ["Quang Hào"], location: "2" },
  { sampleVideo: [manager.sampleVideos.sample, "0:50.5 - 0:53.1"], actors: ["Gia Bảo", "Đại Doãn", "Công Đạt"], preparation: "Trên bảng viết tên 26 bạn nữ", location: "2" },
  { sampleVideo: [manager.sampleVideos.sample, "0:53.3 - 0:56.5"], actors: ["Nguyễn Nhật"], preparation: "TV chiếu hình các bạn nữ", location: "2" },
  { sampleVideo: [manager.sampleVideos.sample, "0:58.6 - 1:00.4"], actors: ["Thành Vũ"], location: "2" },
  { sampleVideo: [manager.sampleVideos.sample, "1:00.8 - 1:02.6"], actors: ["Duy Sơn", "Quang Hào"], preparation: "TV chiếu hình ngôi sao", location: "1" },
  { sampleVideo: [manager.sampleVideos.sample, "1:04.7 - 1:07.7"], actors: ["Thành Vũ", "tất cả"], preparation: "Bảng phụ có nội dung", location: "1" },
  { sampleVideo: [manager.sampleVideos.sample, "1:10.4 - 1:12"], actors: ["Đại Doãn", "Duy Sơn"], preparation: "Một cành hoa (hoặc gì đấy cho giống con gái)", location: "1" },
  { sampleVideo: [manager.sampleVideos.sample, "1:12.3 - 1:13.8"], actors: ["Duy Khang"], preparation: 'Bảng ghi đầy chữ "ngu văn"', location: "1" },
  { sampleVideo: [manager.sampleVideos.sample, "1:18 - 1:19.8"], actors: ["Quang Hào"], location: "1" },
  { sampleVideo: [manager.sampleVideos.sample, "1:23.7 - 1:27.3"], actors: ["Anh Quốc", "Gia Vỹ", "Gia Hưng", "Gia Bảo"], preparation: "1 quyển vở", location: "1" },
  { sampleVideo: [manager.sampleVideos.sample, "1:27.55 - 1:29.8"], actors: ["Xuân Vũ", "Thanh Vũ", "Ngọc Thiện"], preparation: "Đồng hồ (hoặc mở điện thoại)", location: "1" },
  { audio: [manager.audios.audio, "1:42.7 - 1:46.2"], description: "1 người đứng giữa, 4 người đứng xung quanh, lần lượt chạy tới ôm người giữa theo nhạc", actors: ["Đại Doãn", "Ngọc Thiện", "Thanh Vũ", "Trung Nguyên", "Công Đạt"], location: "1" },
  { audio: [manager.audios.audio, "1:50.7 - 1:52.5"], description: "Ghi dang dở bài thơ lên bảng", actors: ["Quang Hào"], preparation: "Ghi dang dở bài thơ tình", location: "1" },
  { audio: [manager.audios.audio, "1:52.7 - 1:53.8"], description: "1 người lấy tay quơ lên đầu người kia (edit gắn nametag trong Minecraft)", actors: ["Chí Vỹ", "Huỳnh Nhật"], location: "1" },
  { sampleVideo: [manager.sampleVideos.sample, "2:12.8 - 2:14"], actors: ["Quang Hào", "Duy Sơn"], location: "1" },
  { audio: [manager.audios.audio, "2:55.1 - 2:58.3"], description: "1 người ngồi trong lớp (gần cửa sổ), người kia thò tay vào để nắm tay, người trong lớp đập tay người bên ngoài, người bên ngoài quắn quéo", actors: ["Thanh Vũ", "Chí Vỹ"], preparation: "1 quyển vở", location: "1" },
  { audio: [manager.audios.audio, "2:58.7 - 3:02.6"], description: "Đập bàn đập ghế", actors: ["Anh Quốc", "Thanh Phú"], location: "1" },
  { audio: [manager.audios.audio, "3:02.8 - 3:06.4"], description: "Ngồi thở dài (2 góc quay)", actors: ["Anh Quốc", "Duy Sơn", "Trung Nguyên"], location: "1" },
  { audio: [manager.audios.audio, "3:06.6 - 3:09"], description: "Ngồi cười khờ", actors: ["Công Đạt"], location: "1" },
  { audio: [manager.audios.audio, "3:09.4 - 3:13.2"], description: "1 người đang đi thì bị người kia đẩy té xuống đè lên, 3 người khác chạy vào đè lên theo nhạc", actors: ["Đại Doãn", "Anh Quốc", "Xuân Vũ", "Thành Vũ", "Huỳnh Nhật"], location: "1" },
  { audio: [manager.audios.audio, "3:13.4 - 3:17"], description: "Đang ở cảnh trên, người bị đè giơ tay lên cầu cứu, thêm 2 người khác nhảy vào đè tiếp", actors: ["Gia Hưng", "Gia Bảo"], location: "1" },
  { audio: [manager.audios.audio, "3:17.2 - 3:19.4"], description: "Chạy nhảy tự do", actors: ["Thanh Vũ", "Ngọc Thiện", "Thanh Phú"], location: "1" },
  { audio: [manager.audios.audio, "3:28.5 - 3:32.5"], description: "Cả đám ngủ (đủ loại tư thế)", actors: ["Tất cả"], location: "1" },
]);

manager.done();
