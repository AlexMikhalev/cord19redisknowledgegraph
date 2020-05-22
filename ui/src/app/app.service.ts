import { Injectable } from '@angular/core';
import {webSocket, WebSocketSubject} from 'rxjs/webSocket';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AppService {
  redisSocket: WebSocketSubject<any> = webSocket(environment.redisUrl);
  constructor() { }
}
