<?php

namespace Funda\Services;

use Doctrine\DBAL\Connection;

class FundaAnalytics
{
    const MAX_RESULTS = 10;

    private $search;
    private $db;
    private $pagination;

    function __construct($search, $db)
    {
        $this->search = $search;

        /** @var Connection $db */
        $this->db = $db;
    }

    public function getTopMakelaars($page = 1)
    {
        $queryBuilder = $this->db->createQueryBuilder();
        $topMakelaars = $queryBuilder
            ->select('MakelaarId', 'MakelaarNaam', 'search', 'count(FundaId) as ItemsListed')
            ->from('listed_objects')
            ->where("search = '$this->search'")
            ->groupBy('MakelaarId')
            ->orderBy('ItemsListed', 'DESC')
            ->setMaxResults(self::MAX_RESULTS)
            ->setFirstResult(self::MAX_RESULTS * ($page - 1))
            ->execute()
            ->fetchAll();
        return $topMakelaars;
    }

    public function countMakelaars()
    {
        $queryBuilder = $this->db->createQueryBuilder();
        $data = $queryBuilder
            ->select('MakelaarId')
            ->from('listed_objects')
            ->where("search = '$this->search'")
            ->groupBy('MakelaarId')
            ->execute()
            ->fetchAll();
        return count($data);
    }

    public function getTopZipcodes($page)
    {
        $queryBuilder = $this->db->createQueryBuilder();
        $topZipcodes = $queryBuilder
            ->select('Postcode', 'search', 'count(FundaId) as ItemsListed')
            ->from('listed_objects')
            ->where("search = '$this->search'")
            ->groupBy('Postcode')
            ->orderBy('ItemsListed', 'DESC')
            ->setMaxResults(self::MAX_RESULTS)
            ->setFirstResult(self::MAX_RESULTS * ($page - 1))
            ->execute()
            ->fetchAll();
        return $topZipcodes;
    }
}