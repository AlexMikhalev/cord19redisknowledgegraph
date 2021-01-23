import { Component, OnInit, ViewChild, ElementRef, HostListener, Output, EventEmitter, Input } from '@angular/core';
import { Observable, of } from 'rxjs';
import SpriteText from 'three-spritetext';
import { UnrealBloomPass } from '../../../../node_modules/three/examples/jsm/postprocessing/UnrealBloomPass.js';
import { MeshBasicMaterial, SphereGeometry, Mesh, Vector2 } from 'three';
import { Store } from '@ngrx/store';
import { State, ISearchResult} from '../../redux/state';
import * as AppSelectors from '../../redux/selectors';
import { filter, distinctUntilChanged, map } from 'rxjs/operators';

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
    this.Graph = ForceGraph3D();
    this.Graph(this.graph.nativeElement)
      .linkDirectionalParticleColor(() => 'red')
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
      .linkHoverPrecision(10)
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
    this.graphClicked.emit({ type: 'node', data: node });
  }

  onLinkClick(node, event){
    this.graphClicked.emit({ type: 'edge', data: node });
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

}
