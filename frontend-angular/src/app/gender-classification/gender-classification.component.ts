import { HttpClient, HttpEventType } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-gender-classification',
  templateUrl: './gender-classification.component.html',
  styleUrls: ['./gender-classification.component.scss']
})
export class GenderClassificationComponent implements OnInit {
  selectedFile: File = null;
  thumbnail: any;
  imageToShow: any;
  isImageLoading: boolean;

  constructor(private http: HttpClient,
    private sanitizer: DomSanitizer) { }

  ngOnInit(): void {
  }

  onFileSelected(event) {
    this.selectedFile = <File>event.target.files[0];
  }

  onUpload() {
    this.imageToShow = null;
    const fd = new FormData();
    fd.append('image', this.selectedFile, this.selectedFile.name);
    this.http.post('http://127.0.0.1:5000/age_gender_detection', fd, {
      reportProgress: true,
      observe: 'events'
    })
      .subscribe(event => {
        if (event.type === HttpEventType.UploadProgress) {
          console.log("Upload Progress: " + Math.round(event.loaded / event.total * 100) + "%")
        }
        else if (event.type === HttpEventType.Response) {
          console.log(event)
        }
        setTimeout(() => {
          this.getImagePrediction()
        }, 1000);
      })
  }

  createImageFromBlob(image: Blob) {
    let reader = new FileReader();
    reader.addEventListener("load", () => {
       this.imageToShow = reader.result;
    }, false);
 
    if (image) {
       reader.readAsDataURL(image);
    }
   }

  getImagePrediction() {
    this.http.get('http://127.0.0.1:5000/age_gender_detection', { responseType: 'blob' })
      .subscribe(data => {
      this.createImageFromBlob(data);
      this.isImageLoading = false;
    }, error => {
      this.isImageLoading = false;
      console.log(error);
    });
}

}
