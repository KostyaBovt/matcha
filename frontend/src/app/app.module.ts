import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';


import { AppComponent } from "./components/layout/app/app.component";
import { HeaderComponent } from './components/layout/header/header.component';
import { NavbarComponent } from './components/layout/navbar/navbar.component';
import { ExploreComponent } from './components/pages/explore/explore.component';
import { ProfileComponent } from './components/pages/profile/profile.component';
import { MessagesComponent } from './components/pages/messages/messages.component';
import { ConnectionsComponent } from './components/pages/connections/connections.component';
import { NotificationsComponent } from './components/pages/notifications/notifications.component';
import { AppRoutingModule } from './/app-routing.module';


@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    NavbarComponent,
    ExploreComponent,
    ProfileComponent,
    MessagesComponent,
    ConnectionsComponent,
    NotificationsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
