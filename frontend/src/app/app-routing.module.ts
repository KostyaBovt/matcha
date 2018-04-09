import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ExploreComponent } from './components/pages/explore/explore.component';
import { ProfileComponent } from './components/pages/profile/profile.component';
import { MessagesComponent } from './components/pages/messages/messages.component';
import { ConnectionsComponent } from './components/pages/connections/connections.component';
import { NotificationsComponent } from './components/pages/notifications/notifications.component';

const routes: Routes = [
  { path: '', redirectTo: '/explore', pathMatch: 'full' },
  { path: 'explore', component: ExploreComponent },
  { path: 'profile', component: ProfileComponent },
  { path: 'messages', component: MessagesComponent },
  { path: 'connections', component: ConnectionsComponent },
  { path: 'notifications', component: NotificationsComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}