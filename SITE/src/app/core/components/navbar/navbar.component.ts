import {Component, EventEmitter, HostListener, Output} from '@angular/core';
import {themeColors} from '../../constants/theme-colors';
import {Color} from '../../enums/colors.enum';
import {MatMenuModule} from "@angular/material/menu";
import {RouterLink, RouterLinkActive} from "@angular/router";
import {NgForOf, NgOptimizedImage} from "@angular/common";
import { MoviesService } from '../../../features/content/services/movies.service';
import { OnTVService } from '../../../features/content/services/onTV.service';
import {MatIconModule} from "@angular/material/icon";
import {MatAnchor, MatIconButton} from "@angular/material/button";
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
  imports: [
    MatMenuModule,
    RouterLinkActive,
    NgOptimizedImage,
    RouterLink,
    MatIconModule,
    NgForOf,
    MatAnchor,
    FormsModule,
    MatIconButton
  ],
  standalone: true
})
export class NavbarComponent {

  @Output() changeColorTheme: EventEmitter<string> = new EventEmitter();
  searchQuery: string = '';
  total: number;
  themeColorList = themeColors;
  themeColorInit: string = Color.PURPLE;

  isScrolled = false;

  searchResults: any[] = []; 
  isLoading = false;

  @HostListener('window:scroll')
  scrollEvent() {
    this.isScrolled = window.scrollY >= 30;
  }

  constructor(
    private movieService: MoviesService,
  ) {}
  
  onSearchQueryChange() {
    console.log('Buscando por:', this.searchQuery);  // Verifique o valor da pesquisa
    if (this.searchQuery.length >= 3) { // Inicia a busca após 3 caracteres
      this.isLoading = true;
      this.searchResults = [];

      // Chama o serviço de filmes
      this.movieService.searchMovies(this.searchQuery, 0).subscribe({
        next: (response) => {
          console.log('Resultados dos filmes:', response);  // Veja o que a API retorna
          this.total = response.length;
          this.searchResults = [...this.searchResults, ...response.results];
          console.log("TETTT", this.total)
          console.log(this.searchResults)
        },
        error: (error) => {
          console.error('Erro ao buscar filmes:', error);
        }
      });
    } else {
      this.searchResults = [];
    }
  }
  
  setColorTheme(color: string) {
    this.themeColorInit = color;
    this.changeColorTheme.emit(color);
  }

}
