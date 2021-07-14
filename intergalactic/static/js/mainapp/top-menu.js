"use strict";

class TopArticles {
    constructor() {
        this.menuTopField = document.querySelector('.content-top-info');
        this.data = [];
        this.render();
        this.refresh();
    }

    async getData() {
        try {
            const response = await fetch(`/get-top-menu/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const res = await response.json();
            // console.log(data, typeof(data))
            const data = await res;
            console.log(data)
            return data
            console.log(this.data)
        } catch (e) {
            console.log(e);
        }
    }

    render() {
        this.data = this.getData();
        // console.log(this.data)
        for(let i = 0; i < this.data.length; i++) {
            console.log(data[i])
            let element = `
            <div class="short-article-field">

                        <div class="short-article-title">
                            <a class="link-top-info-menu" href="{% url 'mainapp:article_detail' ${data[i].id} %}">${data[i].title}</a>
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
                                                    <h5-2-lvc>${data[i].views_number}</h5-2-lvc>
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
                                                    <h5-2-lvc>${data[i].comments_number}</h5-2-lvc>
                                                </li>
                                            </ul>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
            `;
            console.log(element)
            this.menuTopField.insertAdjacentHTML('beforeend', element)
        }
    }

    refresh() {
        setInterval(() => {
            this.render();
        }, 180000)
    }
}
const topMenu = new TopArticles();
