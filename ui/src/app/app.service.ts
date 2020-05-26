import { Injectable } from '@angular/core';
import {webSocket, WebSocketSubject} from 'rxjs/webSocket';
import { environment } from 'src/environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AppService {

  searchSocket: WebSocketSubject<any> = webSocket(environment.redisUrl + '/search');
  graphSocket: WebSocketSubject<any> = webSocket(environment.redisUrl + '/graph');
  
  graphData$: Observable<any>;
  searchData$: Observable<any>;

  constructor() { 

    
    this.searchData$ = this.searchSocket.asObservable();
    this.searchSocket.asObservable().subscribe(dataFromServer => {
      console.log('search data')
      console.log(dataFromServer)
    });

    this.graphData$ = this.graphSocket.asObservable();
    this.graphData$.subscribe(dataFromServer => {
      console.log('graph data')
      console.log(dataFromServer)
    }) 
  }

  search(search){
    this.searchSocket.next({message: search});
  }

  fetchGraph(data){
    this.graphSocket.next({ data: data })
  }
}
