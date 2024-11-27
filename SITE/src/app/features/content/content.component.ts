import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { MoviesService } from './services/movies.service'; // Atualizado para usar MoviesService
import { take } from 'rxjs/operators';
import { Router } from "@angular/router";
import { OnTVService } from "./services/onTV.service";
import { MatPaginatorModule } from "@angular/material/paginator";
import { MovieCardComponent } from "../../shared/components/poster-card-view/poster-card.component";
import { MatButtonModule } from "@angular/material/button";
import { MatCardModule } from "@angular/material/card";
import { TitleCasePipe } from "@angular/common";

@Component({
  selector: 'app-movies',
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.scss'],
  imports: [
    MatPaginatorModule,
    MovieCardComponent,
    MatButtonModule,
    MatCardModule,
    TitleCasePipe
  ],
  standalone: true
})
export class ContentComponent implements OnInit {

  contentType = '';
  nowPlaying: any[] = [];  
  totalResults: any;

  constructor(
    private moviesService: MoviesService,  
    private tvShowsService: OnTVService,
    private router: Router,
    private cdr: ChangeDetectorRef,
  ) {
    this.contentType = this.router.url.split('/')[1];
  }

  ngOnInit() {
    if (this.contentType === 'movies') {
      this.getMovies();  
    } else {
      this.getNowPlayinTVShows(1);  
    }
  }

 
  getMovies() {
    this.moviesService.getMovies().pipe(take(1)).subscribe(
      res => {
        this.totalResults = res.total_results;  
        this.nowPlaying = res.results;  
        this.cdr.detectChanges();
      },
      () => {}
    );
  }

  getNowPlayinTVShows(page: number) {
    this.tvShowsService.getTvOnTheAir(page).pipe(take(1)).subscribe(
      res => {
        this.totalResults = res.total_results;
        this.nowPlaying = res.results;
        this.cdr.detectChanges();
      },
      () => {}
    );
  }

  changePage(event) {
    if (this.contentType === 'movies') {
      this.getMovies(); 
    } else {
      this.getNowPlayinTVShows(event.pageIndex + 1); 
    }
  }
}
