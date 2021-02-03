import { Injectable } from '@angular/core';
import {webSocket, WebSocketSubject} from 'rxjs/webSocket';
import { environment } from 'src/environments/environment';
import { Observable, of } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';

interface ISearchResult{
  links: any[];
  nodes: any[];
}

@Injectable({
  providedIn: 'root'
})
export class AppService {

  // searchSocket: WebSocketSubject<any> = webSocket(environment.redisUrl + '/search');
  // graphSocket: WebSocketSubject<any> = webSocket(environment.redisUrl + '/graph');

  searchUri = 'http://api.thepattern.digital/gsearch'
  
  graphData$: Observable<any>;
  searchData$: Observable<any>;

  constructor(private http: HttpClient) { 
    // this.searchData$ = this.searchSocket.asObservable();
    // this.searchSocket.asObservable().subscribe(dataFromServer => {
    //   console.log('search data')
    //   console.log(dataFromServer)
    // });

    // this.graphData$ = this.graphSocket.asObservable();
    // this.graphData$.subscribe(dataFromServer => {
    //   console.log('graph data')
    //   console.log(dataFromServer)
    // }) 
  }

  // search(search){
  //   this.searchSocket.next({message: search});
  // }

  // fetchGraph(data){
  //   this.graphSocket.next({ data: data })
  // }

  searchApi(text: string): Observable<ISearchResult>{
    return this.http.post<any>(this.searchUri, { search: text }).pipe(map((data) => {
      console.log(data)
      return data.search_result;
    }));
  }

  edgeApi(source: string, target: string): Observable<any>{
    const edgeUri= `http://api.thepattern.digital/edge/edges:${source}:${target}`
    return this.http.get<any>(edgeUri).pipe(map((data) => {
      return data.results;
    }));
  }
}
