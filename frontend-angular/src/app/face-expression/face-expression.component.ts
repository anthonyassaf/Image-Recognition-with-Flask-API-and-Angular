import { HttpClient, HttpEventType } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';
import { ChartData } from '../model/chart-data';
import { ChartImage } from '../model/chart-image';


@Component({
  selector: 'app-face-expression',
  templateUrl: './face-expression.component.html',
  styleUrls: ['./face-expression.component.scss']
})
export class FaceExpressionComponent implements OnInit {

  selectedFile: File = null;
  thumbnail: any;
  imageToShow: any;
  isImageLoading: boolean;
  chartData: ChartData;
  images: ChartImage[] = [];
  baseURL = 'http://127.0.0.1:5000/';

  headers = new Headers({
    'Cache-Control':  'no-cache, no-store, must-revalidate, post- check=0, pre-check=0',
    'Pragma': 'no-cache',
    'Expires': '0'
});

  constructor(private http: HttpClient,
    private sanitizer: DomSanitizer) { }

  ngOnInit(): void {
  }

  onFileSelected(event) {
    this.selectedFile = <File>event.target.files[0];
  }

  onUpload() {
    this.chartData = null
    this.imageToShow = null;
    this.images.length = 0;
    const fd = new FormData();
    fd.append('image', this.selectedFile, this.selectedFile.name);
    this.http.post('http://127.0.0.1:5000/expressions_detection', fd, {
      reportProgress: true,
      observe: 'events'
    })
      .subscribe(event => {
        if (event.type === HttpEventType.UploadProgress) {
        //  console.log("Upload Progress: " + Math.round(event.loaded / event.total * 100) + "%")
        }
        else if (event.type === HttpEventType.Response) {
          //console.log(event)
        }
        setTimeout(() => {
          this.getPrediction();
        }, 5000);
      })
  }

  getPrediction() {
    this.http.get<ChartData>('http://127.0.0.1:5000/expressions_detection')
      .subscribe(data => {
        this.chartData = data;
      
          this.getImages();
      
      }, error => {
        console.log(error);
      });

  }

  getImages(){
    this.images = []
    this.http.get<ChartImage[]>('http://127.0.0.1:5000/image')
      .subscribe(data => {
        this.images = data;
        console.log(data)
      }, error => {
        console.log(error);
      });
  }

  // getHighestPrediction() {
  //   this.http.get('http://127.0.0.1:5000/expressions_detection')
  //     .subscribe(data => {
  //       this.prediction = [].
  // stringify(data)
  //     }, error => {
  //       console.log(error);
  //     });
  // }



}
