import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule }   from '@angular/forms';
import { AgmCoreModule } from '@agm/core';

import {AuthGuard} from './services/auth-guard.service';
import {UserService} from './services/user.service';
import {ProfileService} from './services/profile.service';
import {ExploreService} from './services/explore.service';
import {ApiService} from './services/api.service';


import { AppComponent } from "./components/layout/app/app.component";
import { HeaderComponent } from './components/layout/header/header.component';
import { NavbarComponent } from './components/layout/navbar/navbar.component';
import { ExploreComponent } from './components/pages/explore/explore.component';
import { ProfileComponent } from './components/pages/profile/profile.component';
import { MessagesComponent } from './components/pages/messages/messages.component';
import { ConnectionsComponent } from './components/pages/connections/connections.component';
import { NotificationsComponent } from './components/pages/notifications/notifications.component';
import { MainComponent } from './components/layout/layout/main.component';
import { BlankComponent } from './components/layout/layout/blank.component';
import { AppRoutingModule } from './app-routing.module';
import { LoginComponent } from './components/pages/login/login.component';
import { PageNotFoundComponent } from './components/pages/pagenotfound/pagenotfound.component';
import { RegisterComponent } from './components/pages/register/register.component';
import { ForgotComponent } from './components/pages/forgot/forgot.component';
import { ResetComponent } from './components/pages/reset/reset.component';
import { ConfirmComponent } from './components/pages/confirm/confirm.component';
import { LogoutComponent } from './components/pages/logout/logout.component';
import { ViewComponent } from './components/pages/profile/view/view.component';
import { ModifyComponent } from './components/pages/profile/modify/modify.component';
import { LocationComponent } from './components/pages/profile/location/location.component';
import { PhotosComponent } from './components/pages/profile/photos/photos.component';
import { EmailConfirmComponent } from './components/pages/email-confirm/email-confirm.component';


@NgModule({
  declarations: [
    AppComponent,
    MainComponent,
    BlankComponent,
    PageNotFoundComponent,
    LoginComponent,
    HeaderComponent,
    NavbarComponent,
    ExploreComponent,
    ProfileComponent,
    MessagesComponent,
    ConnectionsComponent,
    NotificationsComponent,
    RegisterComponent,
    ForgotComponent,
    ResetComponent,
    ConfirmComponent,
    LogoutComponent,
    ViewComponent,
    ModifyComponent,
    LocationComponent,
    PhotosComponent,
    EmailConfirmComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    AgmCoreModule.forRoot({
        apiKey: 'AIzaSyAIEehketHiJ7GavS9GkRnUfMN-qNZ-2KU'
    })
  ],
  providers: [AuthGuard, UserService, ProfileService, ApiService, ExploreService],
  bootstrap: [AppComponent]
})
export class AppModule { }
