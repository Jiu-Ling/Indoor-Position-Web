# Description: 图表模板

chartsError = {
                'title': {
                    'text': 'RSS 两模型误差对比图',
                    'left': 'center'
                },
                'tooltip': {
                    'show': True
                },
                'toolbox': {
                    'show': True,
                    'feature': {
                        'saveAsImage': {
                            'pixelRatio': 2
                        }
                    }
                },
                'xAxis': {
                  'type': 'category',
                  'data': 'tmp'
                },
                'yAxis': {
                  'type': 'category',
                  'data': 'tmp'
                },
                'grid': {
                },
                'visualMap': {
                  'min': 0,
                  'max': 8,
                  'calculable': True,
                  'inRange': {
                    'color': [
                      '#313695',
                      '#4575b4',
                      '#74add1',
                      '#abd9e9',
                      '#e0f3f8',
                      '#ffffbf',
                      '#fee090',
                      '#fdae61',
                      '#f46d43',
                      '#d73027',
                      '#a50026'
                    ]
                  }
                },
                'series': [
                  {
                    'name': 'RSS1',
                    'type': 'heatmap',
                    'data': 'tmp',
                    'emphasis': {
                      'itemStyle': {
                        'borderColor': '#333',
                      }
                    },
                    'animation': False
                  },
                  {
                    'type': 'scatter',
                    'data': 'tmp',
                    'symbol':
                      'circle'
                  }
                ]
            }

charts3D = {
            'tooltip': {},
            'toolbox': {
              'show': True,
              'feature': {
                  'saveAsImage': {
                      'pixelRatio': 2,
                  }
              }
            },
            'xAxis3D': {
              'name': 'X',
              'scale': True,
              'type': 'value'
            },
            'yAxis3D': {
              'name': 'Y',
              'scale': True,
              'type': 'value'
            },
            'zAxis3D': {
              'name': 'Z',
              'scale': True,
              'type': 'value'
            },
            'grid3D': {
              'axisLine': {
                'lineStyle': {
                  'color': '#fff'
                }
              },
              'axisPointer': {
                'lineStyle': {
                  'color': '#ffbd67'
                }
              },
              'viewControl': {
              }
            },
            'legend': {
              'show': True,
              'top': '4%'
            },
            'series': [
              {
                'name': 'RSS Results',
                'type': 'scatter3D',
                'dimensions': 'tmp',
                'data': 'tmp',
                'symbolSize': 12,
                'symbol': 'circle',
                'itemStyle': {
                  'borderWidth': 2,
                  'borderColor': 'rgba(255,255,255,0.8)'
                },
                'emphasis': {
                  'itemStyle': {
                    'color': '#fff'
                  }
                }
              },
              {
                'name': 'AP',
                'type': 'scatter3D',
                'dimensions': [
                  'x',
                  'y',
                  'z'
                ],
                'encode': {
                  'x': 'x',
                  'y': 'y',
                  'z': 'z',
                  'tooltip': [0, 1, 2]
                },
                'data': 'tmp',
                'emphasis': {
                  'itemStyle': {
                    'color': '#fff'
                  }
                }
              },
              {
                'name': 'Known Points',
                'type': 'scatter3D',
                'dimensions': [
                  'x',
                  'y',
                  'z'
                ],
                'encode': {
                  'x': 'x',
                  'y': 'y',
                  'z': 'z',
                  'tooltip': [0, 1, 2]
                },
                'data': 'tmp',
                'emphasis': {
                  'itemStyle': {
                    'color': '#fff'
                  }
                }
              }
            ]
          }

visualMap_3D = [
    {
        'show': True,
        'type': 'continuous',
        'dimension': 3,
        'seriesIndex': 0,
        'min': 0,
        'max': 8,
        'inRange': {
            # 'color': [
            #     '#313695',
            #     '#4575b4',
            #     '#74add1',
            #     '#abd9e9',
            #     '#e0f3f8',
            #     '#ffffbf',
            #     '#fee090',
            #     '#fdae61',
            #     '#f46d43',
            #     '#d73027',
            #     '#a50026'
            # ]
            'color': [
                '#313695',
                '#4575b4',
                '#74add1',
                '#abd9e9',
                '#e0f3f8',
                '#ffffbf',
                '#fee090',
                '#fdae61',
                '#f46d43',
                '#d73027',
                '#a50026'
            ]
        }
    }
]