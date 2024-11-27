import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { OnTVService } from '../../services/onTV.service';
import { MoviesService } from '../../services/movies.service';  
import { take } from 'rxjs/operators';
import { MovieCardComponent } from '../../../../shared/components/poster-card-view/poster-card.component';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { TitleCasePipe } from '@angular/common';

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.scss'],
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
  
  isLoading = false;  
  contentType = '';
  movies: any[] = []; 
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
    this.loadContent();  
  }

  loadContent() {
    this.isLoading = true;  
    if (this.contentType === 'movies') {
      this.getMovies(); 
    } else {
     //TODO
    }
  }

  getMovies() {
    this.moviesService.getMovies().pipe(take(1)).subscribe(
      res => {
        this.isLoading = false;  
        this.totalResults = res.total_results;  
        this.movies = res.results;  
        this.cdr.detectChanges();
      },
      () => {
        this.isLoading = false;  
      }
    );
  }

  getNowPlayingTVShows(page: number) {
    this.tvShowsService.getTvOnTheAir(page).pipe(take(1)).subscribe(
      res => {
        this.isLoading = false;  
        this.totalResults = res.total_results;
        this.movies = res.results;  
        this.cdr.detectChanges();
      },
      () => {
        this.isLoading = false; 
      }
    );
  }

  changePage(event) {
    if (this.contentType === 'movies') {
      this.getMovies();  
    } else {
      this.getNowPlayingTVShows(event.pageIndex + 1);  
    }
  }
}
