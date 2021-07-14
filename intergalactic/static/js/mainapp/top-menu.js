"use strict";

class TopArticles {
    constructor() {
        this.menuTopField = document.querySelector('.content-top-info');
        this.topData = [];
        this.render();
        this.refresh();
    };

    render() {
        $.ajax({
            url: '/get-top-menu/',
            type: "GET",
            dataType: "json",
            success: (data) => {
                this.topData = data;
            }
        });
        this.menuTopField.innerHTML = '';
        this.topData.map(el => {
            this.menuTopField.insertAdjacentHTML('beforeend',
                `
                    <div class="short-article-field">

                        <div class="short-article-title">
                            <a class="link-top-info-menu" href="{% url 'mainapp:article_detail' ${el.id} %}">${el['title']}</a>
                        </div>
                        <div class="short-article-data">

                            <div class="like-comment">
                                <ul class="lvc-field">
                                    <li>
                                        <div class="lvc-group">
                                            <ul class="lvc-group">
                                                <li><a href="/"><img src="{% static 'svg/chart.svg' %}" alt="chart"></a>
                                                </li>
                                                <li>
                                                    <h5-2-lvc>over-дохрена</h5-2-lvc>
                                                </li>
                                                <!--<li><a href="/"><img src="svg/down.svg" alt="like"></a></li>-->
                                                <!--<li><h5-2-lvc>-14</h5-2-lchartvc></li>-->
                                            </ul>
                                        </div>
                                    </li>
                                    <li>
                                        <div class="lvc-group">
                                            <ul class="lvc-group">
                                                <li><img src="{% static 'svg/carbon_view-filled_active.svg' %}"
                                                         alt="view"></li>
                                                <li>
                                                    <h5-2-lvc>${el['views_number']}</h5-2-lvc>
                                                </li>
                                            </ul>
                                        </div>
                                    </li>
                                    <li>
                                        <div class="lvc-group">
                                            <ul class="lvc-group">
                                                <li>
                                                    <svg class="icon-comment">
                                                        <use xlink:href="#fluent_comment-24-filled_active"></use>
                                                    </svg>
                                                <li class="comm_number">
                                                    <h5-2-lvc>${el['comments_number']}</h5-2-lvc>
                                                </li>
                                            </ul>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    `)
        });

    };

    refresh() {
        setInterval(() => {
            this.render();
        }, 60000);
    };
}

const topMenu = new TopArticles();
