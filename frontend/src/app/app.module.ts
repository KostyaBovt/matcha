import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule }   from '@angular/forms';

import {AuthGuard} from './services/auth-guard.service';
import {UserService} from './services/user.service';


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
    ResetComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [AuthGuard, UserService],
  bootstrap: [AppComponent]
})
export class AppModule { }
