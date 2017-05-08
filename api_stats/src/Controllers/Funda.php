<?php


namespace Funda\Controllers;


use Exception;
use Funda\Services\FundaAnalytics;
use Funda\Services\PaginationResponse;
use Silex\Application;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;

class Funda
{
    public function topMakelaars(Request $request, Application $app)
    {
        $search = $request->get('search', 'amsterdam');
        $page = $request->get('page', 1);

        $fundaAnalytics = new FundaAnalytics($search, $app['db']);

        try {
            $topMakelaars = $fundaAnalytics->getTopMakelaars($page);
        } catch (Exception $e) {
            return new Response($e->getMessage(), 500);
        }

        $url = sprintf('/funda/topmakelaars?search=%s&page=', $search);
        $topMakelaars['_pagination'] = PaginationResponse::getPaginationValues($url, $page, $fundaAnalytics->countMakelaars());
        return new Response(json_encode($topMakelaars), 200);
    }

    public function topZipcodes(Request $request, Application $app)
    {
        $search = $request->get('search', 'amsterdam');
        $page = $request->get('page', 1);

        try {
            $fundaAnalytics = new FundaAnalytics($search, $app['db']);
            $topZipcode = $fundaAnalytics->getTopZipcodes($page);
            return new Response(json_encode($topZipcode), 200);
        } catch (Exception $e) {
            return new Response($e->getMessage(), 500);
        }
    }
}