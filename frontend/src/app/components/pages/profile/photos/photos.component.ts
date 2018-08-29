import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { ProfileService } from '../../../../services/profile.service';

@Component({
  selector: 'app-photos',
  templateUrl: './photos.component.html',
  styleUrls: ['./photos.component.css']
})
export class PhotosComponent implements OnInit {
  photoName: string = "";
  photoType: string = "";
  photoValue: string = "";
  photoUploaded : number = 0;

  photos: Array<any>;
  loading: number = 0;
  init_loading: number = 0;

  @ViewChild('fileInput') fileInput: ElementRef;

  constructor(private profileService: ProfileService) { }

  ngOnInit() {
    this.loadPhotos();
  }

  loadPhotos() {
    this.init_loading = 1;
    this.profileService.getProfilePhotos().subscribe(response => {
      if (response['success'] == 1) {
        this.photos = response['photos'];
      }
      this.init_loading = 0;
    });
  }

  uploadPhoto() {
    this.loading = 1;
    this.profileService.uploadPhoto(this.photoName, this.photoType, this.photoValue).subscribe(response => {
        if (response['success'] == 1) {
            this.photoUploaded = 1;
            this.resetPhoto();           
            this.loadPhotos();
            this.loading = 0;
        } else {
            alert('cannot upload this photo');
            this.resetPhoto();
            this.loading = 0;
            // this.photoUploaded = 2;
        }
    }, error => {
      // console.log('error status:  ' + error.status);
    });
  }

  resetPhoto() {
    this.fileInput.nativeElement.value = "";
    this.photoName = "";
    this.photoType = "";
    this.photoValue = "";
  }


  onFileChange(event) {
    let reader = new FileReader();
    if(event.target.files && event.target.files.length > 0) {
      let file = event.target.files[0];
      // console.log(file);
      if (file.size > 5 * 1024 * 1024) {
        alert('File is too big! max is 5 mb');
        this.resetPhoto();
      } else if (file.type != "image/jpeg") {
        alert('Invelid file format! only jpeg');
        this.resetPhoto();
      } else {
          reader.readAsDataURL(file);
          reader.onload = () => {
        	this.photoName = file.name;
        	this.photoType = file.type;
        	this.photoValue = reader.result.split(',')[1];
        };
      }
    }
  }

 updateAvatarInArray(photo_hash) {
  this.photos.forEach(function(element) {
    if (element.hash == photo_hash) {
      element.avatar = 1;
    } else {
      element.avatar = 0;
    }
  });
 }

  setAvatar(photo_hash) {
    this.profileService.setAvatar(photo_hash).subscribe(response => {
        if (response['success'] == 1) {
            this.updateAvatarInArray(photo_hash);
        } else {
            alert('Error');
        }
    });
  }


 deletePhotoFromArray(photo_hash) {
  for (var i = this.photos.length - 1; i >= 0; i--) {
    if (this.photos[i].hash == photo_hash) {
      this.photos.splice(i, 1);
    }
  }
 }

  isAvatar(photo_hash) {
    for (var i = 0; i <= this.photos.length - 1; i++) {
      if (this.photos[i].hash == photo_hash && this.photos[i].avatar == 1) {
        return true;
      }
      if (i == this.photos.length - 1) {
        return false;
      }
    }
  }

  getNewFirstAvatarHash() {
    for (var i = 0; i <= this.photos.length - 1; i++) {
      if (this.photos[i].avatar == 0) {
        return this.photos[i].hash;
      }
      if (i == this.photos.length - 1) {
        return this.photos[i].hash;
      }
    }
  }

  deletePhoto(photo_hash) {
    this.profileService.deletePhoto(photo_hash).subscribe(response => {
        if (response['success'] == 1) {
          if (this.isAvatar(photo_hash) && this.photos.length > 1) {
            let newAvatarHash = this.getNewFirstAvatarHash();
            this.profileService.setAvatar(newAvatarHash).subscribe(response => {
                if (response['success'] == 1) {
                    this.updateAvatarInArray(newAvatarHash);
                } else {
                    alert('Error');
                }
            });
          }
          this.deletePhotoFromArray(photo_hash);
        } else {
            alert('Error');
        }
    });
  }


}
