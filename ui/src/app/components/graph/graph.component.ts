import { Component, OnInit, ViewChild, ElementRef, HostListener, Output, EventEmitter, Input } from '@angular/core';
import { Observable, of } from 'rxjs';
import SpriteText from 'three-spritetext';
import { UnrealBloomPass } from '../../../../node_modules/three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { MeshBasicMaterial, SphereGeometry, Mesh, Vector2 } from 'three';
import { Store } from '@ngrx/store';
import { State, ISearchResult} from '../../redux/state';
import * as AppSelectors from '../../redux/selectors';
import { filter, distinctUntilChanged, map } from 'rxjs/operators';
import { Read, Set as SetStoreValue } from 'src/app/redux/actions.js';

declare var ForceGraph3D;
declare var ForceGraphVR;
declare var ForceGraphAR;

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.scss']
})
export class GraphComponent implements OnInit {
  emptySearch = true;
  @ViewChild('graph', { static: true }) graph: ElementRef;
  Graph: any;
  gData: any;
  mode = '3D';
  canvasHeight: number;
  canvasWidth: number;
  sidebarOpen = false;

  @Output() graphClicked: EventEmitter<any> = new EventEmitter();
  @Input() width;
  
  constructor(private store: Store<State>) {
    
  }

  ngOnInit() {
    this.canvasHeight = window.innerHeight - 128;
    this.canvasWidth = window.innerWidth;
    this.store.select<any>(AppSelectors.selectSearchResults)
      .pipe(filter(x => x!=null))
      .subscribe((results) => {
        this.emptySearch = false;
        this.gData = results;
        this.initializeGraph();
      }
    );

    this.store.select(AppSelectors.selectUX)
      .pipe(map(x => x.sidebar))
      .pipe(distinctUntilChanged())
      .pipe(filter(x => x!=null))
      .subscribe(open => {
        console.log(open)
        if(open){
          this.canvasWidth = window.innerWidth - 320;
        }else{
          this.canvasWidth = window.innerWidth;
        }
        
        this.Graph.width(this.canvasWidth)
      }
    );
  }

  initializeGraph() {
    // switch(this.mode){
    //   case '3D':
    //     this.Graph = ForceGraph3D();
    //   case 'VR':
    //     this.Graph = ForceGraphVR();
    //   case 'AR':
    //     console.log('AR mode')
    //     this.Graph = ForceGraphAR();
    //   default:
    //     this.Graph = ForceGraph3D();
    // }
    let highlightNodes = new Set();
    let highlightLinks = new Set();
    this.Graph = ForceGraph3D();
    this.Graph(this.graph.nativeElement)
      // .linkDirectionalParticleColor(() => 'red')
      // .linkDirectionalParticleWidth(4)
      .linkWidth(link => highlightLinks.has(link) ? 4 : 1)
      .linkDirectionalParticles(link => highlightLinks.has(link) ? 4 : 0)
      .linkDirectionalParticleWidth(4)
      .nodeAutoColorBy('rank')
      .nodeThreeObject(node => {
        // use a sphere as a drag handle
        const obj = new Mesh(
          new SphereGeometry(10),
          new MeshBasicMaterial({ depthWrite: false, transparent: true, opacity: 0 })
        );

        // add text sprite as child
        const sprite = new SpriteText(node.name);
        sprite.color = node.color;
        sprite.textHeight = 8;
        obj.add(sprite);

        return obj;
      })
      .linkHoverPrecision(5)
      .onLinkHover(link => {
        highlightNodes.clear();
        highlightLinks.clear();

        if (link) {
          highlightLinks.add(link);
          highlightNodes.add(link.source);
          highlightNodes.add(link.target);
        }

        this.updateHighlight();
      })
      .backgroundColor('#37474f')
      .height(this.canvasHeight)
      .width(this.canvasWidth)
      .graphData(this.gData);

    // this.Graph.onLinkClick(this.Graph.emitParticle); // emit particles on link click
    this.Graph.onNodeClick(this.onNodeClick.bind(this));
    this.Graph.onLinkClick(this.onLinkClick.bind(this));
  }

  @HostListener('window:resize', ['$event'])
  onResize(event) {
    this.canvasHeight = window.innerHeight - 128;
    this.canvasWidth = window.innerWidth;
  }

  onNodeClick(node, event){
    this.onGraphClick({ type: 'node', data: node })
  }

  onLinkClick(node, event){
    this.onGraphClick({ type: 'edge', data: node });
  }

  onLinkHover(node, event){
    this.onGraphClick({ type: 'edge', data: node });
  }

  updateHighlight() {
    // trigger update of highlighted objects in scene
    this.Graph
      .nodeColor(this.Graph.nodeColor())
      .linkWidth(this.Graph.linkWidth())
      .linkDirectionalParticles(this.Graph.linkDirectionalParticles());
  }

  // emitParticles(){
  //   [...Array(10).keys()].forEach(() => {
  //     const link = this.gData.links[Math.floor(Math.random() * this.gData.links.length)];
  //     this.Graph.emitParticle(link);      
  //   });
  //   const modalRef = this.modalService.open(NgbdModalContent);
  //   modalRef.componentInstance.type = 'node';
  // }

  postProcessing(){
    const strength = 0.7;
    const radius = 0.2;
    const threshold = 0;
    const bloomPass = new UnrealBloomPass(new Vector2(128, 128), strength, radius, threshold);
    this.Graph.postProcessingComposer().addPass(bloomPass);
  }

  onGraphClick(event){
    switch(event.type){
      case 'node':
        
        break;

      case 'edge':
        this.store.dispatch(new Read({
          state: 'edgeResults',
          route: `edge/edges:${event.data.source.id}:${event.data.target.id}`
        }));
        this.store.dispatch(new SetStoreValue({
          data: true,
          state: 'sidebar'
        }));

        this.store.dispatch(new SetStoreValue({
          data: event.data,
          state: 'selected'
        }));
        break;

      default:
        break;
    }
  }

}
